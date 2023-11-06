from flask_socketio import SocketIO
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import session

socketio = SocketIO()

MONGODB_URI = 'mongodb://localhost:8080/'
DB_NAME = 'consultoria'

singleton = False
base = None

def get_mongodb_client():
    global base, singleton
    if not singleton:
        base = MongoClient(MONGODB_URI)
        singleton = True
        return base
    else:
        return base


def get_mongodb_db():
    client = get_mongodb_client()
    return client[DB_NAME]


@socketio.on("isAdminAPI")
def isAdmin():
    socketio.emit('isAdminFront', session['admin'])


################################################ ADD / UPDATE ###########################################
def addUser(correo, contraseña, tipo):
    db = get_mongodb_db()
    user = {
        'correo': correo,
        'contraseña': contraseña,
        'tipo': tipo,
    }
    try:
        db.usuarios.insert_one(user)
        return True
    except Exception as e:
        return False

#### GET usuarios name by email
def getUsersEmail(correo):
    db = get_mongodb_db()
    try:
        users = list(db.usuarios.find({'correo': correo}, {'contraseña':1, 'tipo':1}))
        return users
    except Exception as e:
        return None

#### GET usuarios
@socketio.on("usersAPI/get")
def getUsers():
    db = get_mongodb_db()
    try:
        users = list(db.usuarios.findOne({}))
        socketio.emit("usersAPI/get", users)
    except Exception as e:
        socketio.emit("usersAPI", e)


################################################### Solicitudes ###################################################
### Add a solicitud
@socketio.on("requestsAPI/add")
def addRequest(nombre, puesto, departamento, tipo_viaje, pais_destino, motivo, fecha_inicio, fecha_fin, aerolinea, precio_boletos, alojamiento, requiere_transporte):
    try:
        db = get_mongodb_db()
        usuario_id = session['username']
        request_data = {
            'usuario_id': usuario_id,
            'nombre': nombre,
            'puesto': puesto,
            'departamento': departamento,
            'tipo_viaje': tipo_viaje,
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
        db.solicitudes.insert_one(request_data)
        socketio.emit("travelRequestAPI", "Successful")
    except Exception as e:
        socketio.emit("travelRequestAPI", e)

#### Change status
@socketio.on("requestsAPI/estado")
def changeEstado(requestsID, estado):
    db = get_mongodb_db()
    try:
        id_buscado = ObjectId(requestsID)
        estadoUpdate = { "estado" : estado}
        resultado = db.solicitudes.update_one({'_id': id_buscado},{'$set': estadoUpdate})
        if resultado.modified_count == 1:
            socketio.emit("evaluateRequestM", "Successful")
        else:
            socketio.emit("evaluateRequestM", "Error")
    except Exception as e:
        socketio.emit("evaluateRequestM", "Error catch")

### Update a solicitud
@socketio.on("requestsAPI/update")
def addRequest(usuario_id, updated_data):
    db = get_mongodb_db()
    try:
        db.solicitudes.updateOne({'usuario_id': usuario_id},{'$set': updated_data})
        socketio.emit("requestsAPI", "Successful")
    except Exception as e:
        socketio.emit("requestsAPI", e)

##### Get solicitudes

@socketio.on("requestsAPI/getID")
def getRequestID(ID_Find):
    try:
        db = get_mongodb_db()
        id_buscado = ObjectId(ID_Find)
        if session['admin']:
            request = list(db.solicitudes.find({'_id': id_buscado},{'_id':0, 'usuario_id':0}))
            socketio.emit("modifydeleteRequestFront", request)
        else:
            usuario_id = session['username']
            request = list(db.solicitudes.find({'_id': id_buscado, 'usuario_id': usuario_id}, {'_id':0, 'usuario_id':0}))
            socketio.emit("modifydeleteRequestFront", request)
    except Exception as e:
        socketio.emit("modifydeleteRequestFront", "Error")

@socketio.on("requestsAPI/get")
def getRequestID():
    try:
        db = get_mongodb_db()
        if session['admin']:
            requests = list(db.solicitudes.find({},{'usuario_id':0}))
            for i in requests:
                i["_id"] = str(i["_id"])
            socketio.emit("historyRequestFront", requests)
        else:
            usuario_id = session['username']
            requests = list(db.solicitudes.find({'usuario_id': usuario_id}, {'usuario_id':0}))
            socketio.emit("historyRequestFront", requests)
    except Exception as e:
        socketio.emit("historyRequestFront", "Error")

@socketio.on("requestsAPI/getPendientes")
def getPendientesRequest():
    try:
        db = get_mongodb_db()
        if session['admin']:
            requests = list(db.solicitudes.find({'estado':'Pendiente'},{'usuario_id':0}))
            for i in requests:
                i["_id"] = str(i["_id"])
            socketio.emit("evaluateRequestFront", requests)
        else:
            usuario_id = session['username']
            requests = list(db.solicitudes.find({'usuario_id': usuario_id}, {'usuario_id':0}))
            socketio.emit("evaluateRequestFront", requests)
    except Exception as e:
        socketio.emit("evaluateRequestFront", "Error")

#### delete solicitud
@socketio.on("requestsAPI/deleteOne")
def changeEstado(id):
    try:
        db = get_mongodb_db()
        id_buscado = ObjectId(id)
        resultado = db.solicitudes.delete_one({'_id': id_buscado})
        if resultado.deleted_count == 1:
            socketio.emit("modifydeleteRequestFRONT", "Successful")
        else:
            socketio.emit("modifydeleteRequestFRONT", "Error 1")
    except Exception as e:
        print(e)
        socketio.emit("modifydeleteRequestFRONT", "Error catch")

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
        for solicitud in solicitudesAprobadas:
            usuario = db.usuarios.findOne({ 'usuario_id': solicitud['usuario_id'] })
            usuarios.append({
                'nombre': usuario.nombre,
                'Departamento': usuario.departamento
            })
        socketio.emit("scheduledRequestFront", usuarios)
    except Exception as e:
        socketio.emit("scheduledRequestFront", e)

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