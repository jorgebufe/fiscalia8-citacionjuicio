@echo off
title Servidor Fiscalia 8 (no cerrar esta ventana)
cd /d "%~dp0"
echo ==============================================
echo   Servidor Fiscalia 8 citacion juicio
echo ==============================================
echo.

if not exist "%~dp0pocketbase.exe" goto sin_exe
if not exist "%~dp0pb_data" goto sin_datos

echo Direcciones IP de esta PC (anote la IPv4 de su red, ej. 192.168.1.20):
ipconfig | findstr /i "IPv4"
echo.
echo Iniciando el servidor... Cuando aparezca abajo el texto
echo     Server started at http://0.0.0.0:8090
echo el servidor YA ESTA FUNCIONANDO. Es normal que no pase nada mas:
echo la ventana debe quedar abierta (puede minimizarla). NO LA CIERRE.
echo.
"%~dp0pocketbase.exe" serve --http=0.0.0.0:8090
echo.
echo ==============================================
echo   EL SERVIDOR SE DETUVO. Si arriba hay un mensaje de error,
echo   tome una foto o copielo.
echo ==============================================
pause
exit /b 1

:sin_exe
echo ERROR: no se encuentra pocketbase.exe en esta carpeta:
echo    %~dp0
echo.
echo - Si abrio este archivo desde DENTRO del ZIP, primero descomprima:
echo   clic derecho sobre el ZIP - "Extraer todo".
echo - Si el antivirus elimino pocketbase.exe, agregue esta carpeta a las
echo   excepciones del antivirus y vuelva a descomprimir el ZIP.
pause
exit /b 1

:sin_datos
echo ERROR: falta la carpeta pb_data junto a este archivo.
echo Descomprima el ZIP completo (clic derecho - "Extraer todo") y vuelva a intentar.
pause
exit /b 1
