from config import URL
import requests
import json
from pprint import pprint
from get_tasks import Params


def get_all_tasks():
    fields = ["ID", "RESPONSIBLE_ID"]

    params = {}
    task_in_work_params = Params(fields, params)
    task_in_work_params.add_select()
    # task_in_work_params.add_filter('RESPONSIBLE_ID', user_id)
    task_in_work_params.add_filter('<=REAL_STATUS', 4)
    task_in_work_params.add_order('CREATED_DATE', 'asc')
    params = task_in_work_params.get_params()

    print(params)

    method = 'tasks.task.list'
    response = requests.get(f'{URL}/{method}', params=params)
    if response.status_code != 200:
        print('Error')

    content = json.loads(response.content)
    print(len(content.get('result').get('tasks')))
    pprint(content)


def get_task_detail(task_id):


    method = 'tasks.task.get'

    params = {
        "taskId": task_id,
        "descriptionInBbcode": "N",
        "select[0]": "ID",
        "select[1]": "TITLE",
        "select[2]": "STATUS",
        "select[3]": "CREATED_DATE",
        "select[4]": "CREATED_BY",
        "select[5]": "CLOSED_DATE",
        "select[6]": "DEADLINE",
        "select[7]": "DESCRIPTION"
    }

    response = requests.get(f'{URL}/{method}', params=params)

    if response.status_code != 200:
        print(f'Ошибка. Статус={response.status_code}')

    content = json.loads(response.content)
    task = content.get('result').get('task')
    print(task.get('status'))


if __name__ == '__main__':
    # get_task_detail(68077)
    get_all_tasks()
