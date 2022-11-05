# api_yamdb
REST API для сервиса YaMDb. Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». (Совместный проект 3 студентов Яндекс.Практикума)


## Описание

API для сервиса YaMDb предполагает работу со следующими сущностями:

Пользователи (Получить список всех пользователей, создание пользователя, получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username, получить данные своей учетной записи, изменить данные своей учетной записи)

Создание пользователя и получение информации о всех пользователях(GET, POST)

```
http://127.0.0.1:8000/api/v1/users/
```

Получение информации о конкретном пользователе и редактирование информации о нем(GET, POST и DEL)

```
http://127.0.0.1:8000/api/v1/users/{username}/ 
```

Получение и изменение своих данных(GET, PATCH)

```
http://127.0.0.1:8000/api/v1/users/me/
```

Произведения, к которым пишут отзывы (Получить список всех объектов, информация об объекте, создать произведение для отзывов, обновить информацию об объекте, удалить произведение)

Работа с произведениями(GET, POST, PATCH и DEL)

```
http://127.0.0.1:8000/api/v1/titles/
```

Категории (типы) произведений (Получить список всех категорий, создать категорию, удалить категорию)

Работа с категориями(GET, POST и DEL)

```
http://127.0.0.1:8000/api/v1/categories/
```


Категории жанров (Получить список всех жанров, создать жанр, удалить жанр)

Работа с жанрами(GET, POST и DEL)

```
http://127.0.0.1:8000/api/v1/genres/
```

Отзывы (Получить список всех отзывов, создать новый отзыв, получить отзыв по id, частично обновить отзыв по id, удалить отзыв по id)

Коментарии к отзывам (Получить список всех комментариев к отзыву по id, создать новый комментарий для отзыва, получить комментарий для отзыва по id, частично обновить комментарий к отзыву по id, удалить комментарий к отзыву по id)

Работа с отзывами(GET, POST, PATCH и DEL)

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Работа с комментариями(GET, POST, PATCH и DEL)

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

JWT-токен (Отправление confirmation_code на переданный email, получение JWT-токена в обмен на email и confirmation_code)

Получение кода подверждения на email

```
http://127.0.0.1:8000/api/v1/auth/signup/ 
```


```
{
"email": "string",
"username": "string"
}
```

Получение токена для авторизации:

```
http://127.0.0.1:8000/api/v1/auth/token/
```

```
{
"username": "string",
"confirmation_code": "string"
}
```

### [Полная документация API (redoc.yaml)](https://github.com/Filengun/api_yamdb/blob/master/api_yamdb/static/redoc.yaml)
### Либо по документации из API

```
http://127.0.0.1:8000/redoc/
```

## Техническое описание проекта

Клонировать репозиторий и перейти в него

```
git@github.com:Filengun/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv        (для Mac и Linux-систем)
source venv/bin/activate    (для Mac и Linux-систем)
```

```
python -m venv venv         (для Windows-систем)
env/Scripts/activate.bat    (для Windows-систем)
```

Обновить pip:

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate   (для Mac и Linux-систем)
python manage.py migrate    (для Windows-систем)
```

Запустить проект:

```
python3 manage.py runserver (для Mac и Linux-систем)
python manage.py runserver  (для Windows-систем)
```

Перейти в браузере по адресу:

```
http://127.0.0.1:8000
```

## Участники

[Александр](https://github.com/art-bagel) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля.

[Дарья](https://github.com/dmeyker) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них. Рейтинг произведений.

[Олег](https://github.com/Filengun/) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов.

## Слоганы нашей команды
[![Readme Quotes](https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark)](https://github.com/piyushsuthar/github-readme-quotes)