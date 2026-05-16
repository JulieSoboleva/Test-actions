from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Time API", description="Простой тестовый бэкенд с текущим временем сервера")

TIME_FORMATS = (
    "%H:%M",
    "%H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT%H:%M:%S",
)

TIMEZONE_ALIASES: dict[str, str] = {
    "екатеринбург": "Asia/Yekaterinburg",
    "yekaterinburg": "Asia/Yekaterinburg",
    "москва": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "калининград": "Europe/Kaliningrad",
    "kaliningrad": "Europe/Kaliningrad",
    "новосибирск": "Asia/Novosibirsk",
    "novosibirsk": "Asia/Novosibirsk",
    "токио": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "лондон": "Europe/London",
    "london": "Europe/London",
    "нью-йорк": "America/New_York",
    "ньюйорк": "America/New_York",
    "new york": "America/New_York",
    "newyork": "America/New_York",
}


def _normalize_timezone_key(name: str) -> str:
    return name.strip().lower().replace("_", " ")


def resolve_timezone(name: str) -> ZoneInfo:
    key = _normalize_timezone_key(name)
    iana = TIMEZONE_ALIASES.get(key, name.strip())
    try:
        return ZoneInfo(iana)
    except ZoneInfoNotFoundError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Неизвестный часовой пояс: {name!r}. "
            f"Укажите IANA (например Asia/Tokyo) или город из списка алиасов.",
        ) from exc


def parse_utc_datetime(value: str) -> datetime:
    raw = value.strip()
    for fmt in TIME_FORMATS:
        try:
            parsed = datetime.strptime(raw, fmt)
            break
        except ValueError:
            continue
    else:
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Неверный формат времени. Примеры: 15:00, 15:00:00, "
                    "2026-05-16 15:00, 2026-05-16T15:00:00"
                ),
            ) from exc

    if parsed.tzinfo is not None:
        return parsed.astimezone(timezone.utc)

    base_date = date.today()
    if parsed.year == 1900 and parsed.month == 1 and parsed.day == 1:
        parsed = datetime.combine(base_date, time(parsed.hour, parsed.minute, parsed.second))

    return parsed.replace(tzinfo=timezone.utc)


@app.get("/")
def root():
    return {"status": "ok", "message": "Time API is running"}


@app.get("/time")
def get_time():
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now().astimezone()

    return {
        "utc": {
            "server_time": now_utc.isoformat(),
            "timezone": "UTC",
        },
        "local": {
            "server_time": now_local.isoformat(),
            "timezone": str(now_local.tzinfo),
        },
    }


@app.get("/date")
def get_date():
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now().astimezone()

    return {
        "utc": {
            "server_date": now_utc.date().isoformat(),
            "timezone": "UTC",
        },
        "local": {
            "server_date": now_local.date().isoformat(),
            "timezone": str(now_local.tzinfo),
        },
    }


@app.get("/convert")
def convert_time(
    time_value: str = Query(
        ...,
        alias="time",
        description="Время в UTC, например 15:00 или 2026-05-16 15:00:00",
    ),
    timezone_name: str = Query(
        ...,
        alias="timezone",
        description="Часовой пояс: Екатеринбург, Asia/Tokyo и т.д.",
    ),
):
    utc_dt = parse_utc_datetime(time_value)
    target_tz = resolve_timezone(timezone_name)
    converted = utc_dt.astimezone(target_tz)

    return {
        "input_utc": utc_dt.isoformat(),
        "converted": {
            "time": converted.strftime("%H:%M:%S"),
            "datetime": converted.isoformat(),
            "timezone": str(target_tz),
            "timezone_requested": timezone_name,
        },
    }
