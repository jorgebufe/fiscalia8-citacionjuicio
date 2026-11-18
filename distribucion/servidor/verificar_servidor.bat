@echo off
title Verificar servidor Fiscalia 8
echo Probando el servidor en esta PC (http://127.0.0.1:8090)...
curl -s -m 5 http://127.0.0.1:8090/api/health
if errorlevel 1 goto mal
echo.
echo.
echo SERVIDOR FUNCIONANDO. Los clientes deben usar una de estas IP:
ipconfig | findstr /i "IPv4"
pause
exit /b 0

:mal
echo.
echo EL SERVIDOR NO RESPONDE. Abra iniciar_servidor.bat y deje la ventana abierta.
pause
exit /b 1
