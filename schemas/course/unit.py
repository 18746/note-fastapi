from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UnitCreateIn(BaseModel):
    name: str

    is_menu: bool = False
    parent_no: str | None = None
    next_no: str | None = None

class UpdateUnitIn(BaseModel):
    name: str = ""

    is_menu: bool = False
    parent_no: str | None = None
    next_no: str | None = None


class UnitOut(BaseModel):
    course_no: str
    unit_no: str
    name: str

    is_menu: bool
    parent_no: str | None
    next_no: str | None

    create_time: datetime | None = None
    update_time: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    )

