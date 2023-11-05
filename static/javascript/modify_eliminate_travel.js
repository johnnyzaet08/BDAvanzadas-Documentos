const socket = io.connect('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to server, travel request --------');
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

var ID_Find;

function deleteTravelRequest() {
    socket.emit("requestsAPI/deleteOne", ID_Find)
};


function findTravelRequest() {
    ID_Find = nombre = document.getElementById("id").value;
    socket.emit("requestsAPI/getID", ID_Find)
    console.log(ID_Find)
};


window.onload = function() {
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