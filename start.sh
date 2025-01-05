#!/usr/bin/bash

# Start the frontend
cd /home/pi/dashboard/frontend/
npm run dev -- --host &
NPM_PID=$!
echo "NPM-Skript gestartet mit PID $NPM_PID"

# Start the backend
cd /home/pi/dashboard/backend/

source bin/activate
echo "Virtuelle Python-Umgebung aktiviert."
python3 ./main.py &
PYTHON_PID=$!
echo "Python-Skript gestartet mit PID $PYTHON_PID"

wait $NPM_PID
wait $PYTHON_PID