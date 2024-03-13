# Spender: Приложение учета личных финансов 💸
**Spender** - это приложение для учета личных финансов, которое поможет вам эффективно отслеживать ваши доходы и расходы. С легкостью управляйте своим бюджетом, анализируйте траты и принимайте осознанные финансовые решения.

## Используемые технологии
 -   **🐍 Python:** Основной язык программирования.
 -   **🔥 FastAPI:** Web-фреймворк для создания быстрых и современных API.
 -   **🔍 SQLAlchemy и SQLModel:** Инструменты для работы с базой данных и валидации входных и выходных данных.
 -   **🐋 Docker:** Упаковка приложения в контейнер для удобного развертывания.
 -   **🔒 JWT:** Для безопасной аутентификации и авторизации пользователей.
 -   **🤐 Хеширование паролей** для безопасности.
 -   **💾 PostgreSQL:** Реляционная база данных для хранения данных о пользователях, транзакциях и целях.
 -   **📋 Alembic:** Инструмент для управления миграциями базы данных.
 -   **🎻 Poetry:** Инструмент для управления зависимостями и виртуальными окружениями в Python проектах.
 -   **✅ Pytest:** Фреймворк для написания и запуска тестов.
## Основные функции (endpoints)
### Auth
 - POST `auth/login` - Аутентификация пользователя и выдача токена доступа.
 - POST `auth/access-token` - Аутентификация пользователя и выдача токена доступа (вариант для использования в заголовке Authorization).
 - GET `auth/me` - Получение данных текущего авторизованного пользователя.
 
### User
 - GET `user/` - Получение списка пользователей.
 - POST `user/` - Создание нового пользователя.
 - PUT `user/{user_id}`- Обновление данных пользователя.
 - DELETE `user/{user_id}` - Удаление пользователя.

### Account

 - GET `account/{id}` - Получает информацию о счёте по его id.
 - GET  `account/` - Получает список счетов для текущего пользователя.
 - GET `account/get_account_transactions/` - Получает данные о счёте пользователя вместе с его транзакциями.
 - POST `account/` - Создает новый счет для текущего пользователя.
 - PUT `account/{account_id} - Обновляет существующий счет для текущего пользователя.
 - DELETE `account/{account_id}` - Удаляет счет для текущего пользователя.

### Transaction
 - GET `transaction/{id}` - Получает информацию о транзакции по её id.
 - GET `transaction/account_transactions/{account_id}` - Получает список транзакций для указанного счёта с возможностью фильтрации.
 - POST `transaction/` - Создает новую транзакцию для текущего пользователя. Если amount положительная - доход. Если amount отрицательная - расход
 - POST `transaction/transfer_transaction/` - Создает новую транзакцию для перевода денег между счетами текущего пользователя.
 - PUT `transaction/{transaction_id}`- Обновляет существующую транзакцию пользователя.
 - DELETE `transaction/{transaction_id}` - Удаляет транзакцию пользователя.
### Category
 - GET `category/{id}` - Получает информацию о категории по её id.
 - GET`category/` - Получает список категорий для текущего пользователя.
 - POST `category/}`- Создает новую категорию для текущего пользователя.
 - PUT `category/{category_id}`- Обновляет существующую категорию для текущего пользователя.
 - DELETE `category/{category_id}` - Удаляет категорию для текущего пользователя.

### Goal
 - GET `goal/{id}` - Получает информацию о цели по её ID.
 - GET `goal/` - Получает список категорий для текущего пользователя.
 - POST`goal/` - Создает новую цель для текущего пользователя.
 - POST`goal/add_accumulated_amount/{goal_id}` - Добавляет накопленную сумму к текущей сумме цели.
 - PUT `goal/{goal_id}`- Обновляет существующую цель для текущего пользователя.
 - DELETE `goal/{goal_id}` - Удаляет цель текущего пользователя.

### Budget
 - GET `budget/{id}` - Получение информации о конкретном бюджете.
 - GET `budget/` - Получение списка бюджетов пользователя.
 - POST `budget/` - Создание нового бюджета.
 - PUT `budget/{budget_id}`- Обновление информации о бюджете.*
 - DELETE `budget/{budget_id}` - Удаление бюджета.
 
## Установка
 1. Клонируйте репозиторий: `git clone https://github.com/MaksimGMD/spender`
 2. Перейдите в каталог проекта: `cd spender`
 3. Конфигурация.  Создайте `.env` и установите в него основные настройки конфигурации
 - `POSTGRES_USER`
 - `POSTGRES_PASSWORD`
 - `POSTGRES_DB` 
 - `POSTGRES_HOST `
 - `POSTGRES_PORT`
 - `PASSWORD_TEST_USER`
4.  Создайте и запустите контейнер с PostgreSQL: `docker-compose up -d`
5.  Установите зависимости с помощью Poetry: `poetry install`
6.  Выполните миграции базы данных: `alembic upgrade head`
7.  Запустите приложение: `uvicorn app.main:app --reload`

Теперь приложение доступно по адресу `http://127.0.0.1:8000/`. Откройте его в вашем браузере и начните вести учет своих финансов! 🚀
