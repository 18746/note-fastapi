from pydantic import BaseModel
from datetime import datetime
import random

def time_comparison(
    before_time: datetime,
    after_time: datetime = datetime.now(),
    format: str = "%Y-%m-%d %H:%M:%S"
):
    time0 = datetime.strptime(before_time.strftime(format), format)
    time1 = datetime.strptime(after_time.strftime(format), format)
    if time0 > time1:
        return 1
    elif time0 < time1:
        return -1
    else:
        return 0

def get_no(sign: str):
    date_time = datetime.now()
    date_time_strf = date_time.strftime('%Y%m%d%H%M')

    timestamp = date_time.timestamp() * 100

    random.seed(timestamp)
    ran_int = random.randint(100000, 999999)

    return f"{sign}{date_time_strf}{int(ran_int)}"


class UnitFormat(BaseModel):
    state: bool
    message: str = "成功"

if __name__ == '__main__':
    print(get_no("C_"))
    print(type (datetime.now().timetuple()[1]), datetime.now().timetuple())
