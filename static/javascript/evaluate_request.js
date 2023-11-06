window.onload = function() {
    socket.emit('isAdminAPI');
    socket.emit('requestsAPI/getPendientes')
};

socket.on('evaluateRequestM', (message) => {
    if(message == "Successful"){
        window.location.reload();
        alert("Solicitud actualizada exitosamente");
    }else{
        alert(message);
    }
});

socket.on('evaluateRequestFront', (data) => {
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
                ["ID", "Nombre completo", "Puesto", "Departamento", "Internacional", "País de destino", "Motivo del viaje", "Inicio", "Finalización", "Aerolínea", "Precio", "Alojamiento", "Transporte", "Estado", "Proceso"].forEach(function(headerText) {
                    var headerCell = document.createElement("th");
                    headerCell.textContent = headerText;
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

                     // Agrega botones Aceptar y Rechazar
                    var actionsCell = document.createElement("td");
                    var acceptButton = document.createElement("button");
                    acceptButton.textContent = "Aceptar";
                    acceptButton.className = "action-button";
                    acceptButton.addEventListener("click", function() {
                        socket.emit('requestsAPI/estado', rowData["_id"], 'Aprobado')
                    });
                    var rejectButton = document.createElement("button");
                    rejectButton.textContent = "Rechazar";
                    rejectButton.className = "action-button";
                    rejectButton.addEventListener("click", function() {
                        socket.emit('requestsAPI/estado', rowData["_id"], 'Rechazado')
                    });
                    actionsCell.appendChild(acceptButton);
                    actionsCell.appendChild(rejectButton);

                    row.appendChild(actionsCell);
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
