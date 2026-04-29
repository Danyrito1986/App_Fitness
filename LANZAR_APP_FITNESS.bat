@echo off
title App Fitness V7 - PRO
cd /d "%~dp0"

echo ==============================================
echo       APP FITNESS V7 - PRO (MODO ESTABLE)
echo ==============================================
echo.

set VENV_PYTHON=.\.venv\Scripts\python.exe

if not exist %VENV_PYTHON% (
    echo [ERROR] No se encontro el entorno virtual en .venv
    pause
    exit
)

echo Iniciando aplicacion con Python del Entorno Virtual...
%VENV_PYTHON% app_fitness.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] La aplicacion se cerro con errores.
    pause
)
