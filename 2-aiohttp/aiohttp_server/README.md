# Как запустить сервер?

1. Убедиться что установлен Python3 желательно версии 3.9 (проверить версию можно командой `python3 --version`)
2. В этой папке выполнить команды:
   1. `python3 -m venv venv`
   2. `source venv/bin/activate`
   3. `pip install -r requirements.txt`
   4. `python main.py` 

## Методы
1. Создание пользователя: POST http://127.0.0.1:8080/add_user
2. Список пользователей: GET http://127.0.0.1:8080/list_users
3. Получение одного пользователя: GET http://127.0.0.1:8080/get_user
4. Swagger UI http://127.0.0.1:8080/docs
4. Swagger json http://127.0.0.1:8080/docs/json