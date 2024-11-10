from pydantic import BaseModel
from datetime import datetime

class AbsenceLog(BaseModel):
    time: datetime
    message: str