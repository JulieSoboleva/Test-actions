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
| GET   | `/date`   | Текущая дата в UTC и локальной TZ        |
| GET   | `/convert`| Конвертация UTC → указанный часовой пояс |
| GET   | `/docs`   | Swagger UI (автоматически)               |

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

### Пример ответа `GET /date`

```json
{
  "utc": {
    "server_date": "2026-05-16",
    "timezone": "UTC"
  },
  "local": {
    "server_date": "2026-05-16",
    "timezone": "RTZ 2 (зима)"
  }
}
```

### `GET /convert` — конвертация из UTC

Параметры query:

- `time` — время в UTC (`15:00`, `15:00:00`, `2026-05-16 15:00`)
- `timezone` — город или IANA (`Екатеринбург`, `Asia/Tokyo`)

Пример:

```http
GET /convert?time=15:00&timezone=Екатеринбург
```

Ответ:

```json
{
  "input_utc": "2026-05-16T15:00:00+00:00",
  "converted": {
    "time": "20:00:00",
    "datetime": "2026-05-16T20:00:00+05:00",
    "timezone": "Asia/Yekaterinburg",
    "timezone_requested": "Екатеринбург"
  }
}
```

Поддерживаемые алиасы городов: Екатеринбург, Москва, Калининград, Новосибирск, Токио, Лондон, Нью-Йорк (и английские варианты). Также можно передать IANA, например `Europe/Moscow`.
