import requests
import json
from config import URL
from shemas import Task
from config import LOGGER as log
from pydantic import ValidationError


def get_content(request: dict) -> list:
    tasks = []
    match request:
        case {'result': {'tasks': tasks}}:
            pass
    return tasks


class Params:
    def __init__(self, fields: list, params: dict):
        self.fields = fields
        self.params = params

    def add_select(self):
        self.params = dict((f'select{ind}', value) for ind, value in enumerate(self.fields))

    def add_filter(self, field: str, value: int | str):
        self.params[f"filter[{field}]"] = value

    def add_order(self, field: str, value: int | str):
        self.params[f"order[{field}]"] = value

    def get_params(self):
        return self.params


def get_user_tasks(user_id, user, user_list, date1, date2):
    tasks_list = []
    close_tasks_list = []
    deferred_tasks_list = []
    declined_tasks_list = []

    method = 'tasks.task.list'

    fields = ["ID", "TITLE", "STATUS", "CREATED_DATE", "CREATED_BY", "CLOSED_DATE", "DEADLINE", "DESCRIPTION"]

    # Задачи в работе
    params = {}
    task_params = Params(fields, params)
    task_params.add_select()
    task_params.add_filter('RESPONSIBLE_ID', user_id)
    task_params.add_filter('<=REAL_STATUS', 4)
    task_params.add_order('CREATED_DATE', 'asc')
    params = task_params.get_params()

    response = requests.get(f'{URL}/{method}', params=params)

    if response.status_code != 200:
        log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        return tasks_list

    content = json.loads(response.content)

    tasks = get_content(content)

    for data in tasks:
        try:
            task = Task(**data)
        except ValidationError as err:
            log.error(f'Данные задачи не прошли по схеме. {err.json()}')
        else:
            tasks_list.append(task)

    # Завершенные задачи за выбранный период
    params = {}
    task_params = Params(fields, params)
    task_params.add_select()
    task_params.add_filter('RESPONSIBLE_ID', user_id)
    task_params.add_filter('>REAL_STATUS', 4)
    task_params.add_filter('<=REAL_STATUS', 5)
    task_params.add_filter('>=CLOSED_DATE', f"{date1}")
    task_params.add_filter('<=CLOSED_DATE', f"{date2}")
    task_params.add_order('CREATED_DATE', 'asc')
    params = task_params.get_params()

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

    # Отложенные задачи
    params = {}
    task_params = Params(fields, params)
    task_params.add_select()
    task_params.add_filter('RESPONSIBLE_ID', user_id)
    task_params.add_filter('=REAL_STATUS', 6)
    task_params.add_order('CREATED_DATE', 'asc')
    params = task_params.get_params()

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
            deferred_tasks_list.append(task)

    # Отклоненные задачи
    params = {}
    task_params = Params(fields, params)
    task_params.add_select()
    task_params.add_filter('RESPONSIBLE_ID', user_id)
    task_params.add_filter('=REAL_STATUS', 7)
    task_params.add_order('CREATED_DATE', 'asc')
    params = task_params.get_params()

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
            declined_tasks_list.append(task)

    user.TASKS.append(close_tasks_list)
    user.TASKS.append(tasks_list)
    user.TASKS.append(deferred_tasks_list)
    user.TASKS.append(declined_tasks_list)

    user_list.append(user)


if __name__ == '__mane__':
    pass
