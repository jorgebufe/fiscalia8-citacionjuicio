@echo off
title Configurar servidor - Fiscalia 8
cd /d "%~dp0"
echo Escriba la direccion IP de la PC del fiscal (el servidor).
echo Ejemplo: 192.168.1.20
echo.
set /p IP=IP del servidor:
if "%IP%"=="" (
  echo No escribio ninguna IP.
  pause
  exit /b 1
)
>.env echo PB_URL=http://%IP%:8090
echo.
echo Guardado: http://%IP%:8090
echo Probando conexion...
curl -s -m 5 http://%IP%:8090/api/health >nul
if errorlevel 1 (
  echo.
  echo NO SE PUDO CONECTAR. Revise que la IP sea correcta, que el servidor este iniciado
  echo en la PC del fiscal y que se haya ejecutado abrir_firewall.bat en esa PC.
) else (
  echo.
  echo CONEXION OK. Ya puede abrir Fiscalia8.exe
)
pause
