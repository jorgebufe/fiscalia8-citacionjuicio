# Spec Delta

## Purpose

Permite al fiscal registrar causas penales listas para citación a juicio, asignarlas a otras personas para su redacción y seguir su estado hasta que las visa.

## ADDED Requirements

### Requirement: El fiscal registra causas
El sistema SHALL permitir a un admin crear una causa indicando su nombre, que queda en estado "Sin asignar".

#### Scenario: Alta de causa
- **WHEN** el fiscal ingresa un nombre de causa y confirma
- **THEN** la causa aparece en su listado como "Sin asignar"

#### Scenario: Nombre vacío
- **WHEN** el fiscal intenta crear una causa sin nombre
- **THEN** el sistema rechaza el alta y muestra un aviso

### Requirement: El fiscal asigna causas
El sistema SHALL permitir al admin asignar una causa a un usuario activo con rol usuario, y SHALL mostrar a quién está asignada. La causa queda en estado "Esperando".

#### Scenario: Asignación
- **WHEN** el fiscal elige una causa y un usuario y confirma la asignación
- **THEN** el listado del fiscal muestra el nombre del usuario y el estado "Esperando"

#### Scenario: Reasignación
- **WHEN** el fiscal asigna a otro usuario una causa ya asignada
- **THEN** la causa pasa al nuevo usuario y vuelve a "Esperando"

### Requirement: El usuario ve solo sus causas
El sistema SHALL mostrar a cada usuario únicamente las causas que le fueron asignadas.

#### Scenario: Listado propio
- **WHEN** un usuario inicia sesión
- **THEN** ve sus causas asignadas y ninguna de otros usuarios

### Requirement: El usuario confirma recepción
El sistema SHALL permitir al usuario confirmar que vio la causa asignada, pasando de "Esperando" a "En redacción".

#### Scenario: Confirmación
- **WHEN** el usuario confirma la recepción de una causa en "Esperando"
- **THEN** el estado pasa a "En redacción" y el fiscal lo ve reflejado

### Requirement: El usuario avisa que está lista para visado
El sistema SHALL permitir al usuario marcar una causa en redacción como "Lista para visado".

#### Scenario: Marcar lista
- **WHEN** el usuario marca la causa como lista para visado
- **THEN** el estado pasa a "Lista para visado" y queda registrada la fecha

### Requirement: El fiscal visa causas
El sistema SHALL permitir al admin marcar como "Visada" una causa que está "Lista para visado".

#### Scenario: Visado
- **WHEN** el fiscal marca como visada una causa lista para visado
- **THEN** el estado pasa a "Visada"

### Requirement: Un usuario no puede alterar asignaciones
El sistema SHALL impedir que un usuario no admin cambie el nombre, la asignación de una causa o la cree o elimine, y que ponga estados distintos de "En redacción" o "Lista para visado".

#### Scenario: Intento no permitido
- **WHEN** un usuario intenta reasignar o eliminar una causa mediante la API
- **THEN** el servidor rechaza la operación
