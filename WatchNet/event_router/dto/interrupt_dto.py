from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InterruptRequest(BaseModel):
    device_id: str
    interrupt_type: Optional[str] = None
    payload: str
    timestamp: datetime = Field(default_factory=datetime.now)
