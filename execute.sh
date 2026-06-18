#!/bin/bash

kill -9 $(lsof -t -i :5000) 2>/dev/null
kill -9 $(lsof -t -i :5001) 2>/dev/null

echo "Iniciando backend..."
echo
cd backend
source .venv/bin/activate
flask run --debug &

sleep 2
echo
echo "backend iniciado. Iniciando frontend.."
echo

cd ../frontend 
source .venv/bin/activate
flask run --debug --port 5001

echo "Frontend detenido, cerrando backend..."
kill -9 $(lsof -t -i :5000) 2>/dev/null
echo "Backend detenido."