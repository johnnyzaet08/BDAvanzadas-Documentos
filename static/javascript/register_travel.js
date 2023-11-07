socket.on('travelRequestAPI', (message) => {
    if(message == "Successful"){
        document.getElementById("travelRequestForm").reset();
        alert("Solicitud registrada exitosamente");
    }else{
        alert(message);
    }
});

function registerTravelRequest() {
    console.log("xd");
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

    socket.emit("requestsAPI/add", nombre, puesto, departamento, tipo_viaje, pais_destino, motivo, fecha_inicio, fecha_fin, aerolinea, precio_boletos, alojamiento, requiere_transporte);
};

window.onload = function() {
    socket.emit('isAdminAPI');

    var inputs = document.getElementsByClassName('js-input');
    var add_btn = document.getElementById("add-btn");

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('change', myfunc);
    };

    add_btn.addEventListener("click", registerTravelRequest);
}

function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}
