# Design

## Context

Proyecto nuevo, sin código previo, para Windows 10 con Python 3.12 y Tkinter. Varias personas usarán la app con cuentas distintas, por lo que el estado debe estar en un servidor central. Ver proposal.md.

## Goals / Non-Goals

**Goals:**
- App de escritorio simple, sin dependencias de GUI externas.
- Reglas de acceso aplicadas en el servidor (PocketBase), no solo en la interfaz.
- Preparación repetible del backend y un ejecutable único.

**Non-Goals:**
- Redactar o almacenar las citaciones (están en una carpeta compartida externa).
- Notificaciones en tiempo real; la lista se actualiza con un botón y al operar.

## Decisions

- **PocketBase como backend** vía HTTP REST con `requests`. Alternativa: SQLite local; descartada porque varios usuarios necesitan datos compartidos.
- **Tkinter/ttk**: sin dependencias extra y empaquetable con PyInstaller.
- **Colección `users`** (auth) con campos `username`, `rol` (select admin/usuario) y `activo` (bool). Login por `username`; `authRule` = `activo = true` bloquea cuentas desactivadas. Las reglas list/view permiten ver todo solo a admin (cada usuario ve su propio registro); update solo admin; create/delete solo superusuario. El email interno es `<usuario>@fiscalia8.local`.
- **Colección `causas`**: `nombre`, `asignado_a` (relación a users), `estado` (sin_asignar, esperando, en_redaccion, lista_para_visado, visada), `fecha_lista`. Reglas: admin todo; usuario ve y actualiza solo las propias, sin tocar `nombre`/`asignado_a` y con estados limitados a en_redaccion/lista_para_visado.
- **Script `setup_pocketbase.py`**: idempotente, usa el superusuario del `.env` para crear colecciones, reglas y cuentas. Alternativa: migraciones JS de PocketBase; descartada por ser más difícil de generar y verificar.
- **Contraseñas**: todas las cuentas iniciales usan `12345678` (mínimo de PocketBase es 8; decisión del usuario), definida en `.env` como `DEFAULT_USER_PASSWORD`. El superusuario recibe una contraseña aleatoria.
- **`.env`**: `PB_URL`, `PB_SUPERUSER_EMAIL`, `PB_SUPERUSER_PASSWORD`, `DEFAULT_USER_PASSWORD`. La app solo lee `PB_URL`; el `.env` de distribución solo lleva esa variable.
- **Ejecutable**: PyInstaller `--onefile --windowed`. Si `PB_URL` es local y no responde, la app lanza `pocketbase/pocketbase.exe serve` oculto y lo detiene al salir.

## Risks / Trade-offs

- [Contraseñas débiles por pedido] → Panel admin para resetearlas; se documenta la recomendación de cambiarlas.
- [Repo público] → `.env`, `pb_data/` y binarios en `.gitignore`; solo `.env.example` sin valores.
- [PocketBase lanzado desde el exe en cada PC] → Para uso multiusuario se apunta `PB_URL` a un servidor compartido.
- [Archivo `.env` junto al exe visible] → contiene solo la URL.
