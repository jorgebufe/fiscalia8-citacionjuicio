# Tasks

## 1. Git y entorno

- [x] 1.1 Crear `.gitignore` (`.env`, `pocketbase/`, `dist/`, `build/`, `__pycache__`, `.venv`) y verificar con `git status` que no aparecen archivos sensibles
- [x] 1.2 Crear `requirements.txt` e instalar dependencias; verificar `pip list` con requests, python-dotenv, pyinstaller

## 2. PocketBase

- [x] 2.1 Descargar la última versión de PocketBase para Windows en `pocketbase/` y verificar `pocketbase --version`
- [x] 2.2 Crear `.env` y `.env.example`; verificar que `.env.example` no tiene valores y `.env` está ignorado
- [x] 2.3 Crear superusuario, levantar PocketBase y verificar que responde en `/api/health` y `/_/`
- [x] 2.4 Escribir `setup_pocketbase.py` (colecciones, campos, reglas, cuentas) y verificar que es idempotente ejecutándolo dos veces

## 3. Aplicación

- [x] 3.1 Implementar cliente API y manejo de `.env` (`app/api.py`, `app/config.py`) y verificar login con las 5 cuentas
- [x] 3.2 Implementar login y vista del fiscal (causas, asignación, visado) y verificar el flujo end-to-end por API
- [x] 3.3 Implementar vista del usuario (confirmar recepción, marcar lista) y verificar con un script de prueba
- [x] 3.4 Implementar panel admin de cuentas (listar, desactivar, resetear) y verificar con tests de reglas: un usuario no admin es rechazado
- [x] 3.5 Lanzamiento automático de PocketBase y verificación de que la ventana abre sin errores

## 4. Entrega

- [x] 4.1 Script `build.ps1` que genera el `.exe` y arma `dist/`; verificar que el ejecutable inicia
- [x] 4.2 README con instrucciones de uso; verificar que los comandos documentados funcionan
- [x] 4.3 Commit inicial y publicación en GitHub (repo público `fiscalia8-citacionjuicio`)

## 5. Instalación en varias PCs

- [x] 5.1 Separar `build.ps1` en paquetes `dist\Servidor` (PocketBase limpio con cuentas y reglas) y `dist\Cliente` (exe + .env); verificado con `tests.test_flujo` contra el servidor del paquete usando la IP de la red local
- [x] 5.2 Scripts y LEEME de servidor (firewall, inicio con Windows, copias) y de cliente (editar `PB_URL`)
