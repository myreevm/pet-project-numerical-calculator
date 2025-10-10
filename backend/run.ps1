# Создаём виртуальное окружение, если его ещё нет
if (-Not (Test-Path -Path ".\venv")) {
    python -m venv venv
}

# Активируем виртуальное окружение
.\venv\Scripts\Activate.ps1

# Устанавливаем зависимости из requirements.txt
pip install -r requirements.txt

# Запускаем FastAPI с автообновлением
uvicorn app.app:app --reload --port 5000