function searchData () {
    var formContainer = document.getElementById("form-container");
    formContainer.innerHTML = '';

    var search_btn = document.getElementById('find-btn')
    search_btn.addEventListener("click", searchData)

    let mes = document.getElementById("mes").value;
    let ano = document.getElementById("ano").value;

    socket.emit('requestsAPI/programedTravels', mes, ano);
}

window.onload = function() {
    socket.emit('isAdminAPI');
    search_btn = document.getElementById('find-btn');

    search_btn.addEventListener('click', searchData);
};

socket.on('scheduledRequestFront', (data) => {

    if(data == "Error"){
        alert("Error getting information");
    }else{
        try{
            var formContainer = document.getElementById("form-container");
            if(data.length > 0){
    
                var table = document.createElement("table");
                table.className = "data-table";

                // Crea la fila de encabezados de la tabla
                var headerRow = document.createElement("tr");
                ["Nombre completo", "Departamento"].forEach(function(headerText) {
                    var headerCell = document.createElement("th");
                    headerCell.textContent = headerText;
                    // Aplica estilos CSS a las celdas de encabezado
                    headerCell.style.backgroundColor = "lightblue"; // Cambia el color de fondo
                    headerCell.style.color = "black"; // Cambia el color del texto
                    headerRow.appendChild(headerCell);
                });
                table.appendChild(headerRow);
                
                // Itera sobre los datos y crea filas de tabla
                data.forEach(function(rowData) {
                    var row = document.createElement("tr");
                    Object.values(rowData).forEach(function(cellData) {
                        var cell = document.createElement("td");
                        cell.textContent = cellData;
                        row.appendChild(cell);
                    });
                    table.appendChild(row);
                });

                formContainer.appendChild(table);
            } else{
                var message = document.createElement("h1");
                message.textContent = "No posee ningún registro asociado";
                formContainer.appendChild(message);
            }
        } catch (error){
            console.error(error);
            alert("Error loading information");
        }
    }

});