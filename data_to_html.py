from jinja2 import Environment, FileSystemLoader
from config import departments
from datetime import datetime


def save_to_html(date1: str, date2: str):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template('table.html')
    html_text = template.render(date=datetime.now().strftime("%d.%m.%Y"), date1=date1, date2=date2,
                                departments=departments)
    print(html_text)


if __name__ == '__main__':
    ...
