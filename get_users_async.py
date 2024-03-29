import asyncio
import aiohttp
from config import departments, URL
from get_params import Params
from schemas import User
from pydantic import ValidationError
from config import LOGGER as log
from operator import attrgetter


def get_content(request: dict) -> list:
    result = []
    match request:
        case {'result': result}:
            pass
    return result


async def get_users(session, department_id: int):
    method = 'user.get'
    params = {}
    fields = []
    users_list_non_ordered = []
    http_params = Params(fields, params)
    http_params.add_filter('UF_DEPARTMENT', department_id)
    http_params.add_filter('ACTIVE', 'true')
    params = http_params.get_params()
    async with session.request(method='get', url=f'{URL}/{method}', params=params) as response:
        if response.status == 200:
            content = await response.json()
            result = get_content(content)
            for data in result:
                try:
                    user = User(**data)
                    user.departmentId = department_id
                except ValidationError as err:
                    log.error(f'Данные пользователя не прошли по схеме. {err.json()}')
                else:
                    users_list_non_ordered.append(user)
        else:
            log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')
        users_order_list = sorted(users_list_non_ordered, key=attrgetter('LAST_NAME'))
        for user in users_order_list:
            departments[department_id][1].get('users').append(user)


async def gather_users():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for value in departments.values():
            value[1]['users'] = []

        for dep_id in departments.keys():
            task = asyncio.create_task(get_users(session, dep_id))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_users())


if __name__ == '__main__':
    ...
