@echo off

if exist backend\.venv (
    echo Eliminando .venv antiguo en backend...
    rmdir /s /q backend\.venv
)

if exist frontend\.venv (
    echo Eliminando .venv antiguo en frontend...
    rmdir /s /q frontend\.venv
)

cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt

cd ../frontend
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt