# app/grpc_client/client.py
import grpc
from datetime import datetime

try:
    from app.grpc_service.generated import slots_pb2
    from app.grpc_service.generated import slots_pb2_grpc
except ImportError:
    import slots_pb2
    import slots_pb2_grpc


def get_alternatives_via_grpc(restaurant_id: int, start: datetime, end: datetime, guests: int) -> list:
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = slots_pb2_grpc.SlotFinderStub(channel)

        request = slots_pb2.FindSlotsRequest(
            restaurant_id=restaurant_id,
            desired_start=start.isoformat(),
            desired_end=end.isoformat(),
            guests_count=guests,
            limit=3
        )

        try:
            response = stub.FindAlternativeSlots(request, timeout=5.0)

            return [
                {
                    "place_id": s.place_id,
                    "seats": s.seats,
                    "location": s.location,
                    "start_time": s.start_time,
                    "end_time": s.end_time,
                    "shift_minutes": s.shift_minutes
                }
                for s in response.slots
            ]
        except grpc.RpcError as e:
            print(f"[gRPC Client Error] {e.code()} - {e.details()}")
            return []