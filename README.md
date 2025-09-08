<br />
<p align="center">
  <!-- <a href="https://github.com/catiaspsilva/README-template">
    <img src="images/gators.jpg" alt="Logo" width="150" height="150">
  </a> -->

  <h3 align="center">SOCIAL FORUM 
    <br> 
    <span style="font-weight: normal; font-size: 0.8em;">
    microservice system for users communications
    </span>
  </h3>
</p>

## О проекте
Микросервисное приложение, построенное на FastAPI, с поддержкой функций аутентификации, публикации постов и комментариев, сбора статистических данных а также интеграцией с фронтендом на React. Для тестирования предусмотрена возможность генерации синтетических данных.

## Технологии
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.30-FFCA28?style=flat&logo=sqlalchemy)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.2-336791?style=flat&logo=postgresql)
![gRPC](https://img.shields.io/badge/gRPC-1.71.0-6DB33F?style=flat&logo=grpc)
![Kafka](https://img.shields.io/badge/Kafka-3.7.0-231F20?style=flat&logo=apachekafka)
![ClickHouse](https://img.shields.io/badge/ClickHouse-23.3-FFD700?style=flat&logo=clickhouse)
![asyncio](https://img.shields.io/badge/asyncio-3.4.3-3776AB?style=flat)
![Pydantic](https://img.shields.io/badge/Pydantic-2.7.1-0E7C86?style=flat&logo=pydantic)
![Alembic](https://img.shields.io/badge/Alembic-1.13.1-45B8D8?style=flat)
![Pytest](https://img.shields.io/badge/Pytest-8.2.2-0A9EDC?style=flat&logo=pytest)

![JavaScript](https://img.shields.io/badge/JavaScript-ES2023-F7DF1E?style=flat&logo=javascript)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react)


## Схема приложения
![Схема приложения](src/scheme.png)

## Описание основных компонентов

### ProxyService
**Основные возможности:**
- Является API Gateway для всех микросервисов.
- Маршрутизирует HTTP-запросы пользователей к нужным сервисам (Auth, Posts, Stats).
- Реализует базовую аутентификацию: проверяет наличие и валидность токена пользователя.
- Обеспечивает единый вход для фронтенда и внешних клиентов.

### Взаимосвязи:
- Получает запросы от фронтенда/клиентов.
- Перенаправляет запросы на Auth, Posts, Stats в зависимости от типа запроса.
- Может обращаться к Kafka для логирования событий или сбора метрик.

### Auth
**Основные возможности:**
- Регистрация новых пользователей.
- Аутентификация (логин) и выдача токенов доступа.
- Валидация токенов при каждом запросе.
- Обновление профиля пользователя.
- Хранение и управление пользовательскими данными.
- Может поддерживать refresh-токены и logout.

**Взаимосвязи:**
- Получает запросы от Proxy (например, регистрация, логин).
- Проверяет токены для других сервисов (Posts, Stats) через Proxy.
- Может публиковать события в Kafka (например, "user_registered").
- Может обращаться к базе данных пользователей.

### Posts
**Основные возможности:**
-Создание, редактирование и удаление постов.
-Получение списка постов.
-Добавление и удаление комментариев к постам.
-Получение комментариев к конкретному посту.
-Может поддерживать лайки, репосты и другие действия.
-Хранение постов и комментариев.

### Взаимосвязи:
- Получает запросы от Proxy (например, создать пост, получить фид).
- Проверяет права пользователя через Proxy/Auth (например, может ли пользователь создать пост).
- Может публиковать события в Kafka (например, "post_created", "comment_added").
- Может обращаться к Stats для обновления статистики (например, количество постов).

### Stats
**Основные возможности:**
- Сбор и хранение статистики по действиям пользователей (количество постов, комментариев, лайков и т.д.).
- Предоставление агрегированных данных для фронтенда (например, топ-10 пользователей, активность по дням).
- Аналитика по использованию платформы.
- Может поддерживать экспорт данных.

**Взаимосвязи:**
- Получает события из Kafka от других сервисов (Posts, Auth).
- Отвечает на запросы Proxy (например, "показать статистику пользователя").
- Может обращаться к базе данных статистики.
- Может отправлять уведомления или отчёты другим сервисам.

