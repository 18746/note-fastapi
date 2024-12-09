from fastapi import APIRouter, BackgroundTasks, Header, UploadFile, Form
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from utils.pydantic_field import PhoneStrDef

class CourseCreateIn(BaseModel):
    name: str = ''
    type_no: str | None = None

    picture: UploadFile | str = ""
    description: str = ""


class CourseOut(BaseModel):
    course_no: str
    name: str

    picture: str = ""

    type_no: str | None = None
    phone: str = PhoneStrDef("")
    update_num: int = 1
    click_count: int = 1

    description: str = ""

    create_time: datetime | None = None
    update_time: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    )