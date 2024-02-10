from dotenv import load_dotenv
import logging
import os

load_dotenv()

URL = os.environ.get('url')

FILE_LOG = 'bitrix.log'
logging.basicConfig(level=logging.INFO, filename=FILE_LOG,
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
LOGGER = logging.getLogger('wildberries')

departments = {
    233: "Developers",
    235: "Admins",
    237: "Analysts",
    300: "MTD"
}

departments_name = {
    "Developers": "Программисты",
    "Admins": "Администраторы",
    "Analysts": "Аналитики",
    "MTD": "МТО"
}
