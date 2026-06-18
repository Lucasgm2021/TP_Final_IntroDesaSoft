if [ -d "backend/.venv" ]; then
    echo "Eliminando .venv antiguo en backend..."
    rm -rf backend/.venv
fi 

if [ -d "frontend/.venv" ]; then
    echo "Eliminando .venv antiguo en frontend..."
    rm -rf frontend/.venv
fi 

cd backend

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

cd ../frontend 
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt