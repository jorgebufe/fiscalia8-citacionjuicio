# Proposal

## Why

La Fiscalía de Instrucción Nº 8 delega la redacción de las citaciones a juicio a distintas personas, pero hoy no hay un registro de a quién se asignó cada causa ni de cuáles ya están listas para el visado del fiscal. Se necesita una aplicación simple que lleve ese seguimiento.

## What Changes

- Nueva aplicación de escritorio en Python, "Fiscalia 8 citacion juicio", con inicio de sesión por usuario y contraseña.
- El fiscal carga causas, las asigna a un usuario y ve en todo momento a quién se la asignó y en qué estado está.
- Cada usuario ve solo sus causas asignadas, confirma que las recibió y marca cuando la citación está lista para visado.
- Backend con PocketBase; los usuarios tienen un campo `rol` (`admin` / `usuario`) y un campo `activo`.
- Panel de administración (rol admin): listar cuentas, activar/desactivar y resetear contraseña, con reglas de PocketBase que lo restringen a admins.
- Cuentas iniciales: `fiscal` (admin), `Espostodario`, `bufejorge`, `cangijuan`, `turcoalzabe` (usuarios).
- Configuración (URL de PocketBase y contraseñas) en `.env`, con `.env.example` sin valores.
- Ejecutable para Windows con PyInstaller; el repositorio versionado en Git y publicado en GitHub (solo código).

## Capabilities

### New Capabilities
- `gestion-causas`: alta de causas por el fiscal, asignación a un usuario, y seguimiento de estados hasta la visación.
- `cuentas-y-roles`: inicio de sesión, roles, y administración de cuentas (listar, desactivar, resetear contraseña) restringida a admins.

### Modified Capabilities

## Impact

- Código nuevo: aplicación Tkinter en `app/`, script de preparación de PocketBase, script de build.
- Dependencias: PocketBase (binario local), `requests`, `python-dotenv`, `pyinstaller`.
- Sistemas: servidor PocketBase local, repositorio GitHub público.
- Seguridad: las contraseñas iniciales son débiles por pedido del usuario; el `.env` nunca se versiona.
