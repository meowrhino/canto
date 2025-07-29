#!/bin/bash

# Activa el entorno virtual
cd backend
source venv/bin/activate

# Lanza el backend en el puerto 5001 (en background)
echo "Iniciando backend Flask en el puerto 5001..."
python server.py &

BACK_PID=$!

cd ..

# Espera 2 segundos a que el backend arranque
sleep 2

# Lanza el frontend (abre en el navegador por defecto)
cd frontend
echo "Abriendo frontend en http://localhost:8080 ..."
python3 -m http.server 8080 &

FRONT_PID=$!

sleep 2
open "http://localhost:8080"

# Cuando termines, puedes parar ambos procesos con Ctrl+C o cerrando la terminal.
echo "Para cerrar todo: busca y cierra la terminal, o ejecuta: kill $BACK_PID $FRONT_PID"

# Espera para mantener los procesos abiertos
wait
