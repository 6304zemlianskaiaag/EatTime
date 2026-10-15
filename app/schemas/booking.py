from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
class BookingBase(BaseModel):
    place_id: int
    start_time: datetime
    end_time: datetime
    guests_count: int = Field(gt=0)
    comment: Optional[str] = None
class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    comment: Optional[str] = None

class BookingStatusUpdate(BaseModel):
    status: str
class BookingRead(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}