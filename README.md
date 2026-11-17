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

## Ejecutable

```powershell
.\build.ps1
```

Genera `dist\Fiscalia8\Fiscalia8.exe` con la carpeta `pocketbase` al lado. Si `PB_URL` es local y el servidor no está activo, el ejecutable lo inicia solo.

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
