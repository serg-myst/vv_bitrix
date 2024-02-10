from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional, Dict, Union


class Task(BaseModel):
    id: str
    status: int
    title: str
    description: str
    creator: Dict
    createdDate: datetime
    closedDate: Union[datetime, None]

    @validator('status')
    def set_status(cls, s: int) -> str:
        if s == 1:
            return "Новая"
        if s == 2:
            return "Не просмотрена"
        if s == 3:
            return "В работе"
        if s == 4:
            return "Предположительно завершена"
        if s == 5:
            return "Завершена"

class User(BaseModel):
    ID: int
    NAME: str
    LAST_NAME: str
    SECOND_NAME: str
    WORK_POSITION: str
    DATE_REGISTER: datetime
    TASKS: Optional[List[Task]] = []
