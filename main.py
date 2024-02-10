from get_users import get_users_list
from excel import save_to_excel

if __name__ == '__main__':
    result_list = get_users_list()
    save_to_excel(result_list)

# Получить результат выполнения функции из потока
# https://sky.pro/media/poluchenie-vozvrashhaemogo-znacheniya-iz-potoka-v-python/