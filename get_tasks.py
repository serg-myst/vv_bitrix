import requests
import json
from config import URL
from shemas import Task
from config import LOGGER as log
from pydantic import ValidationError


def get_user_tasks(user_id, user, user_list, date1, date2):
    tasks_list = []
    close_tasks_list = []

    method = 'tasks.task.list'

    # Задачи в работе
    params = {
        "filter[RESPONSIBLE_ID]": user_id,
        "filter[<REAL_STATUS]": 4,
        "order[ID]": "desc",
        "select[0]": "ID",
        "select[1]": "TITLE",
        "select[2]": "STATUS",
        "select[3]": "CREATED_DATE",
        "select[4]": "CREATED_BY",
        "select[5]": "CLOSED_DATE",
        "select[6]": "DESCRIPTION"
    }

    response = requests.get(f'{URL}/{method}', params=params)

    if response.status_code != 200:
        log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        return tasks_list

    content = json.loads(response.content)

    for data in content.get('result').get('tasks'):
        try:
            task = Task(**data)
        except ValidationError as err:
            log.error(f'Данные задачи не прошли по схеме. {err.json()}')
        else:
            tasks_list.append(task)

    # Завершенные задачи за выбранный период
    params = {
        "filter[RESPONSIBLE_ID]": user_id,
        "filter[>=REAL_STATUS]": 4,
        "filter[<=REAL_STATUS]": 5,
        "filter[>=CLOSED_DATE]": f"{date1}",
        "filter[<=CLOSED_DATE]": f"{date2}",
        "order[CLOSED_DATE]": "asc",
        "select[0]": "ID",
        "select[1]": "TITLE",
        "select[2]": "STATUS",
        "select[3]": "CREATED_DATE",
        "select[4]": "CREATED_BY",
        "select[5]": "CLOSED_DATE",
        "select[6]": "DESCRIPTION"
    }

    response = requests.get(f'{URL}/{method}', params=params)

    if response.status_code != 200:
        log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        return close_tasks_list

    content = json.loads(response.content)

    for data in content.get('result').get('tasks'):
        try:
            task = Task(**data)
        except ValidationError as err:
            log.error(f'Данные задачи не прошли по схеме. {err.json()}')
        else:
            close_tasks_list.append(task)

    user.TASKS.append(tasks_list)
    user.TASKS.append(close_tasks_list)

    user_list.append(user)


if __name__ == '__mane__':
    pass
