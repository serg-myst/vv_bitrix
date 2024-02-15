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


def get_tasks_by_parameters(params: dict):
    method = 'tasks.task.list'
    response = requests.get(f'{URL}/{method}', params=params)
    if response.status_code != 200:
        log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        return []
    content = json.loads(response.content)
    tasks = get_content(content)
    return tasks


def get_task_list(content: list, result: list) -> list:
    for data in content:
        try:
            task = Task(**data)
        except ValidationError as err:
            log.error(f'Данные задачи не прошли по схеме. {err.json()}')
        else:
            result.append(task)

    return result


def init_params(user_id: int, date1: str, date2: str) -> list:
    param_list = []
    params = {}

    fields = ["ID", "TITLE", "STATUS", "CREATED_DATE", "CREATED_BY", "CLOSED_DATE", "DEADLINE", "DESCRIPTION"]

    task_closed_params = Params(fields, params)
    task_closed_params.add_select()
    task_closed_params.add_filter('RESPONSIBLE_ID', user_id)
    task_closed_params.add_filter('>REAL_STATUS', 4)
    task_closed_params.add_filter('<=REAL_STATUS', 5)
    task_closed_params.add_filter('>=CLOSED_DATE', f"{date1}")
    task_closed_params.add_filter('<=CLOSED_DATE', f"{date2}")
    task_closed_params.add_order('CREATED_DATE', 'asc')

    param_list.append(task_closed_params)

    task_in_work_params = Params(fields, params)
    task_in_work_params.add_select()
    task_in_work_params.add_filter('RESPONSIBLE_ID', user_id)
    task_in_work_params.add_filter('<=REAL_STATUS', 4)
    task_in_work_params.add_order('CREATED_DATE', 'asc')

    param_list.append(task_in_work_params)

    task_deferred_params = Params(fields, params)
    task_deferred_params.add_select()
    task_deferred_params.add_filter('RESPONSIBLE_ID', user_id)
    task_deferred_params.add_filter('=REAL_STATUS', 6)
    task_deferred_params.add_order('CREATED_DATE', 'asc')

    param_list.append(task_deferred_params)

    task_declined_params = Params(fields, params)
    task_declined_params.add_select()
    task_declined_params.add_filter('RESPONSIBLE_ID', user_id)
    task_declined_params.add_filter('=REAL_STATUS', 7)
    task_declined_params.add_order('CREATED_DATE', 'asc')

    param_list.append(task_declined_params)

    return param_list


def get_user_tasks(user_id, user, user_list, date1: str, date2: str):
    param_list = init_params(user_id, date1, date2)

    for par in param_list:
        tasks_list = []
        params = par.get_params()
        result = get_tasks_by_parameters(params)
        tasks_list = get_task_list(result, tasks_list)

        user.TASKS.append(tasks_list)

    user_list.append(user)


if __name__ == '__mane__':
    pass
