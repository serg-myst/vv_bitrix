from config import URL
import requests
import json
from pprint import pprint


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
    get_task_detail(68077)
