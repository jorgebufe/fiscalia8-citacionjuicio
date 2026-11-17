@echo off
title Servidor Fiscalia 8 (no cerrar esta ventana)
cd /d "%~dp0"
echo ==============================================
echo   Servidor Fiscalia 8 citacion juicio
echo   NO CIERRE ESTA VENTANA mientras se trabaja.
echo ==============================================
echo.
echo Direcciones IP de esta PC (use la IPv4 de su red en los clientes):
ipconfig | findstr /i "IPv4"
echo.
echo Los clientes deben usar: PB_URL=http://IP-DE-ESTA-PC:8090
echo Panel de administracion: http://127.0.0.1:8090/_/
echo.
pocketbase.exe serve --http=0.0.0.0:8090
pause
