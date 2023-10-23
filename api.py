from flask_socketio import SocketIO
from pymongo import MongoClient

socketio = SocketIO()

MONGODB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'consultoria'

singleton = False
base = None

def get_mongodb_client():
    global base
    if not singleton:
        base = MongoClient(MONGODB_URI)
        return base
    else:
        return base


def get_mongodb_db():
    client = get_mongodb_client()
    return client[DB_NAME]


################################################ ADD / UPDATE ###########################################

@socketio.on("usersAPI/add")
def addUser(nombre, correo, contraseña, tipo, puesto=None, departamento=None):
    db = get_mongodb_db()
    user = {
        'nombre': nombre,
        'correo': correo,
        'contraseña': contraseña,  # Remember to hash the password
        'tipo': tipo,
        'puesto': puesto,
        'departamento': departamento
    }
    try:
        db.usuarios.insert_one(user)
        socketio.emit("usersAPI", "Successful")
    except Exception as e:
        socketio.emit("usersAPI", e)


@socketio.on("requestsAPI/add")
def addRequest(usuario_id, internacional, pais_destino, motivo, fecha_inicio, fecha_fin, aerolinea, precio_boletos, alojamiento, requiere_transporte):
    db = get_mongodb_db()
    request_data = {
        'usuario_id': usuario_id,
        'internacional': internacional,
        'pais_destino': pais_destino,
        'motivo': motivo,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'aerolinea': aerolinea,
        'precio_boletos': precio_boletos,
        'alojamiento': alojamiento,
        'requiere_transporte': requiere_transporte,
        'estado': 'Pendiente'
    }
    try:
        db.solicitudes.insert_one(request_data)
        socketio.emit("requestsAPI", "Successful")
    except Exception as e:
        socketio.emit("requestsAPI", e)


@socketio.on("usersAPI/get")
def getUsers():
    db = get_mongodb_db()
    try:
        users = list(db.usuarios.find({}))
        socketio.emit("usersAPI/get", users)
    except Exception as e:
        socketio.emit("usersAPI", e)

# You can continue adding more socket endpoints for other functionalities as needed.