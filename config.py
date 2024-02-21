from dotenv import load_dotenv
import logging
import os
from datetime import datetime
import sys

# Настройки для pyinstaller - https://github.com/pyinstaller/pyinstaller/issues/5522

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

URL = os.environ.get('url')

FILE_LOG = 'bitrix.log'
logging.basicConfig(level=logging.INFO, filename=FILE_LOG,
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
LOGGER = logging.getLogger('wildberries')

departments = {
    237: [{'us': "Analysts", 'ru': 'Аналитики', 'order': 1}, {'users': []}],
    235: [{'us': "Admins", 'ru': 'Администраторы', 'order': 2}, {'users': []}],
    233: [{'us': "Developers", 'ru': 'Программисты', 'order': 3}, {'users': []}],
    300: [{'us': "MTD", 'ru': 'Материально-технический отдел', 'order': 4}, {'users': []}]
}

departments_name = {
    'Developers': 'Программисты',
    'Admins': 'Администраторы',
    'Analysts': 'Аналитики',
    'MTD': 'Материально-технический отдел'
}

EMPTY_DATE = datetime.strptime('01.01.2000 00:00:00', '%d.%m.%Y %H:%M:%S')
