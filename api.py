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

#### GET usuarios name by id
@socketio.on("usersAPI/get")
def getUsers(id):
    db = get_mongodb_db()
    try:
        users = list(db.usuarios.find({'id': id}, { nombre:1}))
        socketio.emit("usersAPI/get", users)
    except Exception as e:
        socketio.emit("usersAPI", e)


#### GET usuarios
@socketio.on("usersAPI/get")
def getUsers():
    db = get_mongodb_db()
    try:
        users = list(db.usuarios.findOne({}))
        socketio.emit("usersAPI/get", users)
    except Exception as e:
        socketio.emit("usersAPI", e)


################################################### Solicitudes
### Add a solicitud
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

#### Change status
@socketio.on("requestsAPI/estado")
def changeEstado(usuario_id, estado):
    db = get_mongodb_db()
    try:
        estadoUpdate = { "estado" : estado}
        user =db.solicitudes.updateOne({'usuario_id': usuario_id},{'$set': estadoUpdate})
        socketio.emit("usersAPI/get", user)
    except Exception as e:
        socketio.emit("requestsAPI", e)

### Update a solicitud
@socketio.on("requestsAPI/update")
def addRequest(usuario_id, updated_data):
    db = get_mongodb_db()
    try:
        db.solicitudes.updateOne({'usuario_id': usuario_id},{'$set': updated_data})
        socketio.emit("requestsAPI", "Successful Updated")
    except Exception as e:
        socketio.emit("requestsAPI", e)

##### Get solicitudes
@socketio.on("requestsAPI/get")
def getUsers():
    db = get_mongodb_db()
    try:
        users = list(db.solicitudes.find({}))
        socketio.emit("requestsAPI/get", users)
    except Exception as e:
        socketio.emit("requestsAPI", e)

#### delete solicitud
@socketio.on("requestsAPI/deleteOne")
def changeEstado(usuario_id):
    db = get_mongodb_db()
    try:
        user =db.solicitudes.deleteOne({'usuario_id': usuario_id})
        socketio.emit("requestsAPI", "Successful deleted")
    except Exception as e:
        socketio.emit("requestsAPI", e)

##### consultar un destino especifico
@socketio.on("requestsAPI/getDestine")
def getDestino(destino):
    db = get_mongodb_db()
    try:
        users = list(db.solicitudes.find({'pais_destino': destino}, {fecha_inicio :1,motivo: 1, usuario_id:1 }))
        socketio.emit("requestsAPI/get", users)
    except Exception as e:
        socketio.emit("requestsAPI", e)
    
##### consultar un viajes programados
@socketio.on("requestsAPI/programedTravels")
def getTravels(mes, año):
    db = get_mongodb_db()
    try:
        solicitudesAprobadas =  db.solicitudes.find({'estado': 'Aprobada', 'fecha_inicio': { '$gte': f'{año}-{mes:02d}-01', '$lt': f'{año}-{mes+1:02d}-01'}})
        usuarios =[]
        for solicitud in solicitudes_aprobadas:
            usuario = db.usuarios.findOne({ 'usuario_id': solicitud['usuario_id'] })
            usuarios.append({
                'nombre': usuario.nombre,
                'Departamento': usuario.departamento
            })
        socketio.emit("requestsAPI/get", usuarios)
    except Exception as e:
        socketio.emit("requestsAPI", e)

### Consultar viajes internacionales
@socketio.on("requestsAPI/InternationalTravels")
def getTravelsInternacional(trimestre, año):
    if trimestre == 1:
        start_date = datetime(año, 1, 1)
        end_date = datetime(año, 3, 31)
    elif trimestre == 2:
        start_date = datetime(año, 4, 1)
        end_date = datetime(año, 6, 30)
    elif trimestre == 3:
        start_date = datetime(año, 7, 1)
        end_date = datetime(año, 9, 30)
    elif trimestre == 4:
        start_date = datetime(año, 10, 1)
        end_date = datetime(año, 12, 31)
    else:
        print("Trimestre no válido.")
        return
    try:
        solicitudes_internacionales = db.solicitudes.find({'internacional': True,'fecha_inicio': {'$gte': start_date, '$lte': end_date}})
        usuarios = []
        for solicitud in solicitudes_internacionales:
            usuario = db.usuarios.find_one({'usuario_id': solicitud['usuario_id']})
            if usuario:
                usuarios.append({
                    'nombre' : usuario['nombre'],
                    'pais_destino' : solicitud['pais_destino']
                })
                print(f'Nombre del colaborador: {nombre}, País de destino: {pais_destino}')
        
        socketio.emit("requestsAPI/getInternationalTravels", usuarios)
    except Exception as e:
        socketio.emit("requestsAPI", e)