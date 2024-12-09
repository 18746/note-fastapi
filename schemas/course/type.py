from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TypeCreateIn(BaseModel):
    name: str

class CourseOut(BaseModel):
    type_no: str
    name: str

    create_time: datetime | None = None
    update_time: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    )
