import asyncio
import aiohttp
from config import departments, URL
from get_params import Params
from schemas import User
from pydantic import ValidationError
from config import LOGGER as log


def get_content(request: dict) -> list:
    result = []
    match request:
        case {'result': result}:
            pass
    return result


async def get_users(session, department_id: int, user_list: list):
    method = 'user.get'
    params = {}
    fields = []
    http_params = Params(fields, params)
    http_params.add_filter('UF_DEPARTMENT', department_id)
    http_params.add_filter('ACTIVE', 'true')
    http_params.add_order('LAST_NAME', 'asc')
    params = http_params.get_params()
    async with session.request(method='get', url=f'{URL}/{method}', params=params) as response:
        if response.status == 200:
            content = await response.json()
            result = get_content(content)
            for data in result:
                try:
                    user = User(**data)
                except ValidationError as err:
                    log.error(f'Данные пользователя не прошли по схеме. {err.json()}')
                else:
                    user_list.append(user)
        else:
            log.error(f'Ошибка получения данных методом {method}. Статус {response.status_code}')


async def gather_users() -> list:
    users_list = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for dep_id in departments.keys():
            task = asyncio.create_task(get_users(session, dep_id, users_list))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return users_list


def main():
    asyncio.run(gather_users())


if __name__ == '__main__':
    ...
