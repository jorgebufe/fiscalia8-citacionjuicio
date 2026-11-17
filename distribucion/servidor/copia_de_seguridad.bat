@echo off
rem Copia los datos (causas y cuentas) a la carpeta "copias" con fecha. Cierre el servidor antes.
cd /d "%~dp0"
set "FECHA=%date:~-4%%date:~3,2%%date:~0,2%"
xcopy /e /i /y pb_data "copias\pb_data_%FECHA%" >nul
echo Copia creada en copias\pb_data_%FECHA%
pause
