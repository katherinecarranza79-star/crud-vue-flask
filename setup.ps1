# Instalación inicial en Windows (PowerShell). Ejecutar desde la carpeta crud-vue-flask:
#   .\setup.ps1
$ErrorActionPreference = "Stop"

Write-Host "== Backend ==" -ForegroundColor Cyan
Set-Location "$PSScriptRoot\backend"
py -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
& .\.venv\Scripts\python.exe -m flask --app run.py db upgrade

Write-Host "== Frontend ==" -ForegroundColor Cyan
Set-Location "$PSScriptRoot\frontend"
npm install
if (-not (Test-Path .env)) { Copy-Item .env.example .env }

Write-Host "Listo. Use .\iniciar.ps1 para abrir ambos servidores." -ForegroundColor Green
