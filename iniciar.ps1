# Abre el backend (Flask, puerto 5000) y el frontend (Vite, puerto 5173) en dos ventanas.
$root = $PSScriptRoot
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; .\.venv\Scripts\Activate.ps1; flask --app run.py run --debug"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"
Start-Process "http://localhost:5173"
