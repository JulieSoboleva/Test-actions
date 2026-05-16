from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Time API", description="Простой тестовый бэкенд с текущим временем сервера")


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
