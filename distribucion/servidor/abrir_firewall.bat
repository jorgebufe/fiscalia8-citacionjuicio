@echo off
rem Permite que las otras PCs de la red lleguen al servidor (puerto 8090).
net session >nul 2>&1
if errorlevel 1 (
  echo Ejecute este archivo con clic derecho - "Ejecutar como administrador".
  pause
  exit /b 1
)
netsh advfirewall firewall delete rule name="Fiscalia8 PocketBase" >nul 2>&1
netsh advfirewall firewall add rule name="Fiscalia8 PocketBase" dir=in action=allow protocol=TCP localport=8090
echo.
echo Listo: puerto 8090 habilitado.
pause
