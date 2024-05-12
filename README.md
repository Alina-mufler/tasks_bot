# Tasks bot project

Простой телеграм бот для добавления задач и их просмотра.

БД: PostgreSQL

### Настройка проекта

Для настройки проекта выполните следующие шаги:

1. Клонируйте репозиторий:
git clone
2. Перейдите в директорию проекта
3. Скопируйте `.env.example` в новый файл `.env` и заполните необходимые значения переменных окружения:
cp .env.example .env ([Как заполнить переменные окружения?](#Description_env) )
4. Установите зависимости: 
```pip install -r requirements.txt```
5. Запустите проект:
```python tasks.py```


#### <a id="Description_env">Описание переменных окружения</a>
TOKEN - для его получения необходимо создать свой телеграм бот: 

1. Перейти по ссылке и создать бота: [@BotFather](https://t.me/BotFather)
2. Скопировать полученный токен в .env файл

DATABASE_URL - ссылка на базу данных в формате 
```text 
"postgresql://username:password@localhost:port/databasename"
```

## Тестирование проекта 

| Действие                                        |    Команда    |
|-------------------------------------------------|:-------------:|
| Добавить задачу                                 | /add <задача> |
| Получить все задачи                             |  кнопка /tsk  | |


