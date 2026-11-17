# Spec Delta

## Purpose

Define el inicio de sesión, los roles de usuario y la administración de cuentas, restringida a administradores.

## ADDED Requirements

### Requirement: Inicio de sesión por usuario
El sistema SHALL autenticar con nombre de usuario y contraseña, y SHALL rechazar credenciales inválidas.

#### Scenario: Credenciales correctas
- **WHEN** un usuario activo ingresa usuario y contraseña correctos
- **THEN** accede a la aplicación con las vistas de su rol

#### Scenario: Credenciales incorrectas
- **WHEN** se ingresa una contraseña errónea
- **THEN** el sistema muestra un error y no inicia sesión

### Requirement: Cuentas iniciales
El sistema SHALL contar con las cuentas `fiscal` (rol admin) y `Espostodario`, `bufejorge`, `cangijuan`, `turcoalzabe` (rol usuario), creadas por un script repetible.

#### Scenario: Preparación repetida
- **WHEN** se ejecuta el script de preparación más de una vez
- **THEN** no se duplican cuentas ni colecciones

### Requirement: Roles
Cada cuenta SHALL tener un rol `admin` o `usuario`; solo un admin puede cambiar roles.

#### Scenario: Vistas por rol
- **WHEN** inicia sesión un admin
- **THEN** ve el panel de causas del fiscal y el panel de cuentas
- **WHEN** inicia sesión un usuario
- **THEN** ve solo sus causas asignadas

### Requirement: Panel de cuentas para admins
El sistema SHALL mostrar a un admin la lista de cuentas con su rol y estado, y permitir desactivar/reactivar cuentas y resetear su contraseña.

#### Scenario: Desactivar cuenta
- **WHEN** el admin desactiva una cuenta
- **THEN** esa cuenta ya no puede iniciar sesión

#### Scenario: Resetear contraseña
- **WHEN** el admin ingresa una nueva contraseña válida para una cuenta
- **THEN** la cuenta puede iniciar sesión con la nueva contraseña

#### Scenario: Auto-desactivación
- **WHEN** el admin intenta desactivar su propia cuenta
- **THEN** la aplicación lo impide

### Requirement: Reglas del servidor restringen la administración
El servidor SHALL permitir listar todas las cuentas, desactivarlas y resetear contraseñas únicamente a admins; un usuario solo puede ver su propia cuenta.

#### Scenario: Usuario intenta administrar
- **WHEN** un usuario no admin consulta la lista de cuentas o modifica otra cuenta por API
- **THEN** el servidor no devuelve otras cuentas y rechaza la modificación
