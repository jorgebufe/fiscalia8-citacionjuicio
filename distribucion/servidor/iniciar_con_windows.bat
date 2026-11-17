@echo off
rem Crea un acceso directo en Inicio para que el servidor arranque al iniciar sesion en Windows.
set "DESTINO=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Servidor Fiscalia 8.lnk"
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%DESTINO%'); $s.TargetPath='%~dp0iniciar_servidor.bat'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()"
echo Listo: el servidor se iniciara solo (minimizado) al abrir sesion en esta PC.
pause
