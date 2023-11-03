const socket = io.connect('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to server, travel request --------');
});
window.onload = function() {
    var esFalso = true; // Cambiar a true o false según sea necesario
    var travelForm = document.getElementById("travelForm");
    // Acceder a los valores de los campos de formulario
    if (!esFalso) {
        travelForm.style.display = 'none';
    }else{
        travelForm.style.display = 'block'; 
    }
};