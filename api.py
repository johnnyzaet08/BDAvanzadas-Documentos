from flask_socketio import SocketIO
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
from flask import session

socketio = SocketIO(cors_allowed_origins="*")

MONGODB_URI = 'mongodb://192.168.100.7:27017/'
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
        print("xd")
        date_format = "%Y-%m-%d"
        fecha_inicio_covert = datetime.strptime(fecha_inicio, date_format)
        fecha_fin_covert = datetime.strptime(fecha_fin, date_format)

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
            'fecha_inicio': fecha_inicio_covert,
            'fecha_fin': fecha_fin_covert,
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
        print(e)
        socketio.emit("evaluateRequestM", "Error catch")

### Update a solicitud
@socketio.on("requestsAPI/update")
def addRequest(request_id, nombre, puesto, departamento, tipo_viaje, pais_destino, motivo, fecha_inicio, fecha_fin, aerolinea, precio_boletos, alojamiento, requiere_transporte):
    db = get_mongodb_db()
    try:
        date_format = "%Y-%m-%d"
        fecha_inicio_covert = datetime.strptime(fecha_inicio, date_format)
        fecha_fin_covert = datetime.strptime(fecha_fin, date_format)

        id_buscado = ObjectId(request_id)
        request_data = {
            'nombre': nombre,
            'puesto': puesto,
            'departamento': departamento,
            'tipo_viaje': tipo_viaje,
            'pais_destino': pais_destino,
            'motivo': motivo,
            'fecha_inicio': fecha_inicio_covert,
            'fecha_fin': fecha_fin_covert,
            'aerolinea': aerolinea,
            'precio_boletos': precio_boletos,
            'alojamiento': alojamiento,
            'requiere_transporte': requiere_transporte,
            'estado': 'Pendiente'
        }
        resultado = db.solicitudes.update_one({'_id': id_buscado, 'usuario_id': session['username']},{'$set': request_data})
        socketio.emit("requestsAPI", "Successful")
        if resultado.modified_count == 1:
            socketio.emit("modifydeleteRequestM", "Successful")
        else:
            socketio.emit("modifydeleteRequestM", "Error")
    except Exception as e:
        socketio.emit("modifydeleteRequestM", "Error Catch")

##### Get solicitudes

@socketio.on("requestsAPI/getID")
def getRequestID(ID_Find):
    try:
        db = get_mongodb_db()
        id_buscado = ObjectId(ID_Find)
        if session['admin']:
            request = list(db.solicitudes.find({'_id': id_buscado},{'_id':0, 'usuario_id':0}))
            for i in request:
                i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
                i['fecha_fin'] = i['fecha_fin'].strftime("%Y-%m-%d")
            socketio.emit("modifydeleteRequestFront", request)
        else:
            usuario_id = session['username']
            request = list(db.solicitudes.find({'_id': id_buscado, 'usuario_id': usuario_id}, {'_id':0, 'usuario_id':0}))
            for i in request:
                i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
                i['fecha_fin'] = i['fecha_fin'].strftime("%Y-%m-%d")
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
                i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
                i['fecha_fin'] = i['fecha_fin'].strftime("%Y-%m-%d")
            socketio.emit("historyRequestFront", requests)
        else:
            
            usuario_id = session['username']
            requests = list(db.solicitudes.find({'usuario_id': usuario_id}, {'usuario_id':0}))
            for i in requests:
                i["_id"] = str(i["_id"])
                i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
                i['fecha_fin'] = i['fecha_fin'].strftime("%Y-%m-%d")
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
                i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
                i['fecha_fin'] = i['fecha_fin'].strftime("%Y-%m-%d")
            socketio.emit("evaluateRequestFront", requests)
        else:
            usuario_id = session['username']
            requests = list(db.solicitudes.find({'usuario_id': usuario_id}, {'usuario_id':0}))
            for i in requests:
                i["_id"] = str(i["_id"])
                i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
                i['fecha_fin'] = i['fecha_fin'].strftime("%Y-%m-%d")
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
        users = list(db.solicitudes.find({'pais_destino': destino}, {'nombre':1, 'fecha_inicio':1, 'motivo': 1, '_id':0 }))
        for i in users:
            i['fecha_inicio'] = i['fecha_inicio'].strftime("%Y-%m-%d")
        socketio.emit("specificRequestFront", users)
    except Exception as e:
        socketio.emit("specificRequestFront", "Error")
    
##### consultar un viajes programados
@socketio.on("requestsAPI/programedTravels")
def getTravels(mes, año):
    try:
        mes = int(mes)
        año = int(año)
        db = get_mongodb_db()
        fecha_inicio = datetime(año, mes, 1)
        if mes == 12:
            fecha_fin = datetime(año + 1, 1, 1)  # Año nuevo si es diciembre
        else:
            fecha_fin = datetime(año, mes + 1, 1)

        solicitudesAprobadas = list(db.solicitudes.find({'estado': 'Aprobado','fecha_inicio': {'$gte': fecha_inicio, '$lte': fecha_fin}}, {'nombre':1, 'pais_destino':1, '_id':0}))
        socketio.emit("scheduledRequestFront", solicitudesAprobadas)

    except Exception as e:
        socketio.emit("scheduledRequestFront", "Error")

### Consultar viajes internacionales
@socketio.on("requestsAPI/InternationalTravels")
def getTravelsInternacional(trimestre, año):
    try:
        db = get_mongodb_db()
        trimestre = int(trimestre)
        año = int(año)
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

        solicitudes_internacionales = list(db.solicitudes.find({'tipo_viaje': 'internacional','fecha_inicio': {'$gte': start_date, '$lte': end_date}}, {'nombre':1, 'pais_destino':1, '_id':0}))
        socketio.emit("internationalRequestFront", solicitudes_internacionales)
    except Exception as e:
        socketio.emit("internationalRequestFront", "Error")