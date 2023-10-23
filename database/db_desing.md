# Colección: Usuarios

- **id**: ObjectId - Identificador único del usuario.
- **nombre**: String - Nombre completo del usuario.
- **correo**: String - Correo electrónico del usuario.
- **contraseña**: String - Contraseña hash del usuario.
- **tipo**: String - Tipo de usuario (colaborador o administrativo).
- **puesto**: String - Puesto del colaborador (solo para colaboradores).
- **departamento**: String - Departamento para el que trabaja (solo para colaboradores).

# Colección: Solicitudes

- **id**: ObjectId - Identificador único de la solicitud.
- **usuario_id**: ObjectId - Referencia al usuario que hizo la solicitud.
- **internacional**: Boolean - Indica si el viaje es internacional o no.
- **pais_destino**: String - País de destino del viaje.
- **motivo**: String - Motivo del viaje (seguimiento, cierre venta, capacitación).
- **fecha_inicio**: Date - Fecha de inicio del viaje.
- **fecha_fin**: Date - Fecha de finalización del viaje.
- **aerolinea**: String - Nombre de la aerolínea.
- **precio_boletos**: Number - Precio de los boletos.
- **alojamiento**: String - Nombre del alojamiento.
- **requiere_transporte**: Boolean - Indica si requiere transporte.
- **estado**: String - Estado de la solicitud (Pendiente, Aprobada, Rechazada).

# Colección: Administrativos

- **id**: ObjectId - Identificador único del administrativo.
- **usuario_id**: ObjectId - Referencia al usuario administrativo.
- **funciones**: Array - Lista de funciones o responsabilidades del administrativo.
