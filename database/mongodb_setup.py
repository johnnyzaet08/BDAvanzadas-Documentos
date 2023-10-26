from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('localhost', 27017)

# Creación de la base de datos 'consultoria'
db = client['consultoria']

# Creación de la colección 'usuarios'
usuarios = db['usuarios']

# Creación de la colección 'solicitudes'
solicitudes = db['solicitudes']

# Creación de la colección 'administrativos'
administrativos = db['administrativos']

# # Insertar un usuario de ejemplo
# usuarios.insert_one({
#     'nombre': 'Juan Pérez',
#     'correo': 'juan.perez@example.com',
#     'contraseña': 'hashed_password',  # Recuerda usar un hash real
#     'tipo': 'colaborador',
#     'puesto': 'Gerente',
#     'departamento': 'Ventas'
# })

# Inserta una nueva solicitud
solicitud_nueva = {
    'tipo': 'vacaciones',
    'fecha_inicio': '2023-11-01',
    'fecha_fin': '2023-11-07',
    'estado': 'pendiente',
    'empleado_id': 1
}

solicitudes.insert_one(solicitud_nueva)

# Inserta un nuevo registro administrativo
administrativo_nuevo = {
    'nombre': 'Nombre del administrativo',
    'cargo': 'Cargo del administrativo',
    'departamento': 'Departamento del administrativo'
}

administrativos.insert_one(administrativo_nuevo)

print('Base de datos y colecciones creadas exitosamente.')