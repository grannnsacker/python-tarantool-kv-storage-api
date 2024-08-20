# FastAPI kv-store with Tarantool

## Описание

Данный проект представляет собой FastAPI приложение, использующее Tarantool в качестве базы данных. В этом репозитории вы найдете инструкции по запуску приложения, документирование API и тесты.

## Инструкция к установки

Для запуска проекта вам потребуется Python и Docker.

### 1. Клонирование репозитория

```git clone https://github.com/grannnsacker/python-tarantool-kv-storage-api.git```

### 2. Настройка переменных окружения
####Необходимо настроить переменные среды окружения для корректной работы приложения.
####Добавьте в .env следующие переменные (внизу продемонстрированы переменные с примерами):
```
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
DB_USERNAME=sampleuser
DB_PASSWORD=samplepassword
DB_HOST=tarantool
DB_PORT=3301
TEST_DB_HOST=test_tarantool
TEST_DB_PORT=3302
```

### 3. Запуск приложения
```
docker compose up app
```

## Документация API
## /api/login

### Метод: Post
### Описание: Аутентификация пользователя
### Примеры запросов:
#### 1) Успешная авторизация
```json
{
  "username": "admin",
  "password": "presale"
}
```
### Ответ:
#### 200 OK
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzI0MTc5MTEyfQ.5JcuUoibq-flYnT69sF3T6eOOgE2fXg6vH-XdSvnNZ4"
}
```
### Примеры возможных ошибок:
#### 401 Unauthorized: Неверные данные авторизации.
```json
{
  "detail": "Incorrect user data"
}
```
#### 422 Unprocessable Entity: Неверный формат данных.
``` json
{
  "detail": [
    {
      "type": "string_type",
      "loc": [
        "body",
        "username"
      ],
      "msg": "Input should be a valid string",
      "input": []
    }
  ]
}
```
#### 500 Internal Server Error: Ошибка базы данных.
```json
{
  "detail": "Database connection error"
}
```
##
## /api/write
### Метод: Post
### Описание: Запись данных в kv-хранилище
#### При повторном обращениии по тому же ключу - значение заменяется на последнее.
### Примеры запросов:
#### 1) Успешная запись пачкой
```json
{
  "data": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```
#### Ответ:
#### 200 OK
```json
{
  "status": "success"
}
```
#### 2) Успешная запись
```json
{
  "data": {
    "key1": "value1"
  }
}
```
#### Ответ:
#### 200 OK
```json
{
  "status": "success"
}
```

#### Возможные ошибки
#### 401 Unauthorized: Неверные данные авторизации.
```json
{
  "detail": "Invalid authorization token"
}
```
#### 422 Unprocessable Entity: Неверный формат данных.
```json
{
  "detail": [
    ...
  ]
}
```
#### 500 Internal Server Error: Ошибка базы данных.
```json
{
  "detail": "Database connection error"
}
```
##
## /api/read
### Метод: Post
### Описание: Чтение данных из kv-хранилища
### Примеры запросов:
#### 1) Успешное чтение 1 значения
```json
{
  "keys": ["key1"]
}
```
#### Ответ:
#### 200 OK
```json
{
  "data": {
    "key1": "value1"
  }
}
```
#### 2) Успешное чтение пачки значений
```json
{
  "keys": ["key1", "key2"]
}
```
#### Ответ:
#### 200 OK
```json
{
  "data": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

#### 3) Ненаход значений
##### Если значение не найдено, то вместо value будет возвращен null. В рамках одного запроса допускается получения существующих и не существующих значений.
```json
{
  "keys": ["key1", "key3"]
}
```
#### Ответ:
#### 200 OK
```json
{
  "data": {
    "key1": "value1",
    "key3": null
  }
}
```


#### Возможные ошибки
#### 401 Unauthorized: Неверные данные авторизации.
```json
{
  "detail": "Invalid authorization token"
}
```
#### 422 Unprocessable Entity: Неверный формат данных.
```json
{
  "detail": [
    ...
  ]
}
```
#### 500 Internal Server Error: Ошибка базы данных.
```json
{
  "detail": "Database connection error"
}
```

#### Для интерактивного ознакомления с документацией рекомендуется воспользоваться UI SWAGGER'ом. После запуска приложения перейдите по "/docs"

##
## Тестирование
#### Все тест находятся в папочке app/tests
#### Для запуска тестов необходимо написать следующую команду:
``` 
docker-compose up test_app test_tarantool --abort-on-container-exit --exit-code-from test_app
```
#### После, запустится два контейнера: с тестами и с тестовой базой данных, а затем сами тесты.
#### Всего существут 8 тестов:
#### api/login
#### 1) Тест на успешную авторизацию
#### 2) Тест на неуспешную авторизацию (неверный юзернейм)
#### 3) Тест на неуспешную авторизацию (неверный пароль)
##
#### api/read
#### 1) Тест на мульти-чтение
#### 2) Тест на чтение несуществующего объекта
##
#### api/write
#### 1) Тест на успешную мульти-запись
#### 2) Тест на успешную сингл-запись
#### 3) Тест на неуспешную запись


## База данных
#### Все файлы, связанные с базой данных находятся в db/
#### Для рабочего приложения в db/app
#### Там находятся два файла config.yaml и myapp.lua
##
#### Для тестов в db/test
#### Главное различие в том, что данные из тестовой бд удаляются при каждом запуске, для корректного тестирования.
