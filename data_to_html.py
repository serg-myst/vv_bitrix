from jinja2 import Environment, FileSystemLoader
from config import departments
from datetime import datetime
import shutil


def save_to_html(date1: str, date2: str, catalog: str, label):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template('table.html')
    html_text = template.render(date=datetime.now().strftime("%d.%m.%Y"), date1=date1, date2=date2,
                                departments=departments)
    filename = f'{catalog}/Задачи_{datetime.today().strftime("%Y_%m_%d")}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_text)
        label.config(text=f'Отчет сформирован {filename}', fg='#A9A9A9', anchor='w')
        shutil.copyfile('templates/style.css', f'{catalog}/style.css')


if __name__ == '__main__':
    ...
