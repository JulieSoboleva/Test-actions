# Time API

Простой тестовый бэкенд на FastAPI, возвращающий текущее время сервера в UTC и в локальной временной зоне.

## Установка

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

## Эндпоинты

| Метод | Путь   | Описание                          |
|-------|--------|-----------------------------------|
| GET   | `/`    | Проверка, что сервер работает     |
| GET   | `/time`| Текущее время в UTC и локальной TZ|
| GET   | `/docs`| Swagger UI (автоматически)        |

### Пример ответа `GET /time`

```json
{
  "utc": {
    "server_time": "2026-05-16T12:00:00.123456+00:00",
    "timezone": "UTC"
  },
  "local": {
    "server_time": "2026-05-16T15:00:00.123456+03:00",
    "timezone": "RTZ 2 (зима)"
  }
}
```
