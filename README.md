# Fiscalia 8 citacion juicio

Aplicación de escritorio (Python + Tkinter) para que el fiscal de instrucción asigne causas listas para citación a juicio a otras personas, y siga su estado hasta el visado. Backend: [PocketBase](https://pocketbase.io).

## Flujo

1. El fiscal (admin) carga la causa y la asigna a un usuario → estado **Esperando**.
2. El usuario inicia sesión, ve la causa y confirma la recepción → **En redacción**.
3. Redacta la citación (en la carpeta compartida, fuera de la app) y la marca **Lista para visado**.
4. El fiscal ve cuáles están listas, las revisa y las marca **Visada**.

El rol `admin` además tiene un panel de **Cuentas**: listar, activar/desactivar y resetear contraseña.

## Puesta en marcha

```powershell
pip install -r requirements.txt
copy .env.example .env        # completar los valores
# Descargar PocketBase (Windows) en la carpeta pocketbase/ y crear el superusuario:
pocketbase\pocketbase.exe superuser upsert <PB_SUPERUSER_EMAIL> <PB_SUPERUSER_PASSWORD>
pocketbase\pocketbase.exe serve --http=127.0.0.1:8090   # panel: http://127.0.0.1:8090/_/
python setup_pocketbase.py    # colecciones, reglas, hooks y cuentas iniciales
python main.py
```

Reiniciá PocketBase después de `setup_pocketbase.py` para que cargue los hooks.

Cuentas iniciales: `fiscal` (admin), `Espostodario`, `bufejorge`, `cangijuan`, `turcoalzabe`, todas con la contraseña `DEFAULT_USER_PASSWORD` del `.env`. **Cambialas** desde el panel de cuentas.

## Instalación en varias PCs

```powershell
.\build.ps1
```

Genera dos paquetes en `dist\` (no se versionan):

- `dist\Servidor`: PocketBase limpio (colecciones, reglas, hook y las 5 cuentas) para la **PC del fiscal**, que queda encendida. Incluye `iniciar_servidor.bat`, `abrir_firewall.bat` (ejecutar como administrador una vez), `iniciar_con_windows.bat` y `copia_de_seguridad.bat`. Escucha en `0.0.0.0:8090`.
- `dist\Cliente`: `Fiscalia8.exe` y un `.env` con solo `PB_URL`. Se copia a cada PC (incluida la del fiscal) y se edita `PB_URL` con la IP de la PC del fiscal, por ejemplo `http://192.168.1.20:8090`. Reservar esa IP en el router.

Para trabajar desde fuera de la oficina sin abrir puertos al internet, usar [Tailscale](https://tailscale.com) en el servidor y en esa PC, y poner la IP `100.x.x.x` del servidor en `PB_URL`.

Si el `.exe` encuentra una carpeta `pocketbase` al lado y `PB_URL` es local, inicia PocketBase solo (modo una sola PC).

## Pruebas

```powershell
python -c "from dotenv import load_dotenv; load_dotenv(); import runpy; runpy.run_module('tests.test_flujo', run_name='__main__')"
```

## Variables (.env)

| Variable | Uso |
| --- | --- |
| `PB_URL` | Dirección de PocketBase |
| `PB_SUPERUSER_EMAIL` / `PB_SUPERUSER_PASSWORD` | Superusuario, solo para `setup_pocketbase.py` |
| `DEFAULT_USER_PASSWORD` | Contraseña inicial de las cuentas |

El `.env`, `pocketbase/`, `dist/` y `build/` no se versionan. Los cambios se planifican con OpenSpec (`openspec/`).
