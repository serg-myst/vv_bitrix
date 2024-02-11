import xlwt
from config import departments_name
from datetime import datetime
from operator import attrgetter


def save_to_excel(data, catalog, label):
    book = xlwt.Workbook(encoding='utf-8')

    sheet1 = book.add_sheet("tasks")

    num = 0
    for dep in data:
        for key, value in dep.items():
            row = sheet1.row(num)
            row.write(0, departments_name.get(key))
            num += 1
            value = sorted(value, key=attrgetter('LAST_NAME'))
            for user in value:
                row = sheet1.row(num)
                row.write(0, f'{user.LAST_NAME} {user.NAME} {user.SECOND_NAME}')
                num += 1
                row = sheet1.row(num)
                row.write(0, f'№ Задачи')
                row.write(1, f'Статус')
                row.write(2, f'Название')
                row.write(3, f'Постановщик')
                row.write(4, f'Дата создания')
                row.write(5, f'Дата закрытия')
                num += 1
                for task_list in user.TASKS:
                    for task in task_list:
                        row = sheet1.row(num)
                        row.write(0, f'{task.id}')
                        row.write(1, f'{task.status}')
                        row.write(2, f'{task.title}')
                        row.write(3, f'{task.creator.get("name")}')
                        row.write(4, f'{task.createdDate.strftime("%Y-%m-%d")}')
                        if task.closedDate:
                            row.write(5, f'{task.closedDate.strftime("%Y-%m-%d")}')
                        num += 1

                row = sheet1.row(num)
                row.write(0, '')
                num += 1

    try:
        filename = f'Задачи_{datetime.today().strftime("%Y_%m_%d")}.xls'
        book.save(f'{catalog}/{filename}')
        label.config(text=f'Отчет сформирован {catalog}/{filename}', fg='#A9A9A9', anchor='w')
    except PermissionError as Er:
        label.config(text=f'Ошибка формирования отчета {Er}', fg='#FF0000', anchor='w')


if __name__ == '__main__':
    save_to_excel('')
