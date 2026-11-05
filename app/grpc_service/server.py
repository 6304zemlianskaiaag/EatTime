# app/grpc_service/server.py
import grpc
from concurrent import futures
from datetime import datetime
from sqlalchemy import select, and_
import time

from app.db import SessionLocal
from app.models import Place, TableType, Booking, BookingStatus

from app.grpc_service.generated import slots_pb2
from app.grpc_service.generated import slots_pb2_grpc


class SlotFinderServicer(slots_pb2_grpc.SlotFinderServicer):

    def FindAlternativeSlots(self, request, context):
        print(f"[gRPC Server] Начинаю обработку запроса... ")
        time.sleep(3)
        print(f"[gRPC Server] Закончил обработку!")
        print(f"\n[gRPC Server] Получен запрос:")
        print(f"  restaurant_id = {request.restaurant_id}")
        print(f"  desired_start = {request.desired_start}")
        print(f"  guests_count  = {request.guests_count}")

        session = SessionLocal()
        try:
            start = datetime.fromisoformat(request.desired_start)
            end = datetime.fromisoformat(request.desired_end)

            # (seats >= guests)
            places = session.scalars(
                select(Place).join(Place.table_type).where(
                    Place.restaurant_id == request.restaurant_id,
                    Place.is_active.is_(True),
                    TableType.seats >= request.guests_count
                )
            ).all()

           # response = slots_pb2.FindSlotsResponse()

            #  свободно ли время
            count = 0
            for place in places:
                conflict = session.scalar(
                    select(Booking).where(
                        Booking.place_id == place.id,
                        Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
                        and_(Booking.start_time < end, Booking.end_time > start)
                    )
                )
                if conflict is None:
                    count += 1
                    print(f" Отправляю столик #{place.id} (мест: {place.table_type.seats})")
                    yield slots_pb2.Slot(
                            place_id=place.id,
                            seats=place.table_type.seats,
                            location=place.table_type.location.value,
                            start_time=start.isoformat(),
                            end_time=end.isoformat()
                        )


        finally:
            session.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    slots_pb2_grpc.add_SlotFinderServicer_to_server(SlotFinderServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server запущен на порту 50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()