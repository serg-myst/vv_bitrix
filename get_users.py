import requests
import json
from shemas import User
from config import URL
from config import LOGGER as log
from pydantic import ValidationError
from config import departments
from get_tasks import get_user_tasks
import threading

RESULT_LIST = []


def add_users(department_number, department_name):
    method = 'user.get'
    user_list = []
    params = {
        "order[LAST_NAME]": "asc",
        "filter[UF_DEPARTMENT]": department_number,
        "filter[ACTIVE]": "true"
    }

    response = requests.get(f'{URL}/{method}', params=params)

    if response.status_code != 200:
        log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        return user_list

    content = json.loads(response.content)

    for data in content.get('result'):
        thread_task_lis = []
        try:
            user = User(**data)
        except ValidationError as err:
            log.error(f'Данные пользователя не прошли по схеме. {err.json()}')
        else:
            thread_task_lis.append(threading.Thread(target=get_user_tasks, args=(user.ID, user, user_list)))
            # thread_task_lis.append(threading.Thread(target=get_user_closed_tasks, args=(user.ID, user, user_list)))

        for thread in thread_task_lis:
            thread.start()

        for t in thread_task_lis:
            t.join()

    RESULT_LIST.append({department_name: user_list})

    # return user_list


def get_users_list():
    thread_list = []
    for dep, value in departments.items():
        thread_list.append(threading.Thread(target=add_users, args=(dep, value,)))

    for thread in thread_list:
        thread.start()

    for t in thread_list:
        t.join()

    return RESULT_LIST


if __name__ == '__main__':
    ul = get_users_list()

