### Учебный проект "Продуктовый Помощник"
Автор: Швейников Андрей
Cтудент когорты №25 Python-разработчик. Яндекс.Практикум.

### Адрес сервера
51.250.106.127

### Состояние воркфлоу
![example workflow](https://github.com/xxxRichiexxx/foodgram-project-react/actions/workflows/for_main_branche_workflow.yml/badge.svg)

### Краткое описание
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Для репозитория настроен CI/CD. Для запуска приложения:

Сделайте Fork данного репозитория
Подготовьте vps с ubuntu и docker
Добавьте action secrets под Ваш проект:
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
PASSPHRASE
POSTGRES_DB
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY
TELEGRAM_TO
(кому отправить сообщение о статусе ci/cd workflow)
TELEGRAM_TOKEN
(токен вашего телеграм бота)
USER
(пользователь на хосте)
