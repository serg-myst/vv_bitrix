import requests
import json
from schemas import User
from config import URL
from config import LOGGER as log
from pydantic import ValidationError
from config import departments
from get_tasks import get_user_tasks
import threading

RESULT_LIST = []


def get_content(request: dict) -> list:
    result = []
    match request:
        case {'result': result}:
            pass
    return result


def add_users(department_number, department_name, date1, date2):
    method = 'user.get'
    user_list = []
    params = {
        "filter[UF_DEPARTMENT]": department_number,
        "filter[ACTIVE]": "true"
    }

    response = requests.get(f'{URL}/{method}', params=params)

    if response.status_code != 200:
        log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        return user_list

    content = json.loads(response.content)

    result = get_content(content)

    for data in result:
        thread_task_list = []
        try:
            user = User(**data)
        except ValidationError as err:
            log.error(f'Данные пользователя не прошли по схеме. {err.json()}')
        else:
            thread_task_list.append(
                threading.Thread(target=get_user_tasks, args=(user.ID, user, user_list, date1, date2)))

        for thread in thread_task_list:
            thread.start()

        for t in thread_task_list:
            t.join()

    RESULT_LIST.append({department_name: user_list})


def get_users_list(date1, date2):
    thread_list = []
    RESULT_LIST.clear()
    for dep, value in departments.items():
        thread_list.append(threading.Thread(target=add_users, args=(dep, value, date1, date2,)))

    for thread in thread_list:
        thread.start()

    for t in thread_list:
        t.join()

    return RESULT_LIST


if __name__ == '__main__':
    pass
