socket.on('modifydeleteRequestFRONT', (message) => {
    if(message == "Successful"){
        document.getElementById("travelRequestForm").reset();
        alert("Solicitud eliminada exitosamente");
    }else{
        alert(message);
    }
});

function modifyTravelRequest() {
    let nombre = document.getElementById("nombre").value;
    let puesto = document.getElementById("puesto").value;
    let departamento = document.getElementById("departamento").value;
    let tipo_viaje = document.getElementById("tipo_viaje").value;
    let pais_destino = document.getElementById("pais_destino").value;
    let motivo = document.getElementById("motivo").value;
    let fecha_inicio = document.getElementById("fecha_inicio").value;
    let fecha_fin = document.getElementById("fecha_fin").value;
    let aerolinea = document.getElementById("aerolinea").value;
    let precio_boletos = document.getElementById("precio_boletos").value;
    let alojamiento = document.getElementById("alojamiento").value;
    let requiere_transporte = document.getElementById("requiere_transporte").value;

    socket.emit("travelRequestAPI/add", nombre, puesto, departamento, tipo_viaje, pais_destino, motivo, fecha_inicio, fecha_fin, aerolinea, precio_boletos, alojamiento, requiere_transporte);
};

socket.on('modifydeleteRequestFront', (data) => {
    document.getElementById("nombre").value = data[0]['nombre'];
    document.getElementById("puesto").value = data[0]['puesto'];
    document.getElementById("departamento").value = data[0]['departamento'];
    document.getElementById("tipo_viaje").value = data[0]['tipo_viaje'];
    document.getElementById("pais_destino").value = data[0]['pais_destino'];
    document.getElementById("motivo").value = data[0]['motivo'];
    document.getElementById("fecha_inicio").value = data[0]['fecha_inicio'];
    document.getElementById("fecha_fin").value = data[0]['fecha_fin'];
    document.getElementById("aerolinea").value = data[0]['aerolinea'];
    document.getElementById("precio_boletos").value = data[0]['precio_boletos'];
    document.getElementById("alojamiento").value = data[0]['alojamiento'];
    document.getElementById("requiere_transporte").value = data[0]['requiere_transporte'];
});

var ID_Find;

function deleteTravelRequest() {
    socket.emit("requestsAPI/deleteOne", ID_Find)
};


function findTravelRequest() {
    var in_find = document.getElementById("id_input").value;
    ID_Find = in_find;
    socket.emit("requestsAPI/getID", in_find)
};


window.onload = function() {
    socket.emit('isAdminAPI');
    
    var esFalso = true; // Cambiar a true o false según sea necesario
    var travelForm = document.getElementById("travelForm");
    
    var inputs = document.getElementsByClassName('js-input');

    var modify_btn = document.getElementById("modify-btn");
    var delete_btn = document.getElementById("delete-btn");
    var find_btn = document.getElementById("find-btn");
    
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('change', myfunc);
    };

    modify_btn.addEventListener("click", modifyTravelRequest);
    delete_btn.addEventListener("click", deleteTravelRequest);
    find_btn.addEventListener("click", findTravelRequest);

    // Acceder a los valores de los campos de formulario
    if (!esFalso) {
        travelForm.style.display = 'none';
    }else{
        travelForm.style.display = 'block'; 
    }
};

function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}