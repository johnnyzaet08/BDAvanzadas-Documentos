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

# Insertar un usuario de ejemplo
usuarios.insert_one({
    'nombre': 'Juan Pérez',
    'correo': 'juan.perez@example.com',
    'contraseña': 'hashed_password',  # Recuerda usar un hash real
    'tipo': 'colaborador',
    'puesto': 'Gerente',
    'departamento': 'Ventas'
})

print('Base de datos y colecciones creadas exitosamente.')