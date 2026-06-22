@echo off

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5001') do taskkill /f /pid %%a 2>nul

echo Iniciando backend...
echo.
cd backend
call .venv\Scripts\activate
start /b flask run --debug

timeout /t 3 /nobreak >nul
echo.
echo backend iniciado. Iniciando frontend..
echo.

cd ../frontend
call .venv\Scripts\activate
flask run --debug --port 5001

echo.
echo Frontend detenido, cerrando backend...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do taskkill /f /pid %%a 2>nul
echo Backend detenido.