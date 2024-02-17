from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional, Dict, Union


class Task(BaseModel):
    id: int
    status: int
    status_btx: int = Field(alias='status')
    status_real: int = Field(alias='status')
    title: str
    description: str
    creator: Dict
    createdDate: datetime
    closedDate: Union[datetime, None]
    deadline: Union[datetime, None]

    @field_validator('status')
    def set_status(cls, s: int) -> str:
        match s:
            case 1:
                return "В работе"
            case 2:
                return "В работе"
            case 3:
                return "В работе"
            case 4:
                return "В работе"
            case 5:
                return "Завершена"
            case 6:
                return "Отложена"
            case 7:
                return "Отклонена"
            case _:
                return "Не определено"

    @field_validator('status_btx')
    def set_btx_status(cls, s: int) -> str:
        match s:
            case 1:
                return "STATE_NEW"
            case 2:
                return "STATE_PENDING"
            case 3:
                return "STATE_IN_PROGRESS"
            case 4:
                return "STATE_SUPPOSEDLY_COMPLETED"
            case 5:
                return "STATE_COMPLETED"
            case 6:
                return "STATE_DEFERRED"
            case 7:
                return "STATE_DECLINED"
            case _:
                return "Не определено"


class User(BaseModel):
    ID: int
    NAME: str
    LAST_NAME: str
    SECOND_NAME: str
    WORK_POSITION: str
    DATE_REGISTER: datetime
    TASKS: Optional[List[Task]] = []
