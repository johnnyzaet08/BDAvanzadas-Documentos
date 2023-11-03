const socket = io.connect('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to server, travel request --------');
});
window.onload = function() {
    var esFalso = true; // Cambiar a true o false según sea necesario
    var formContainer = document.getElementById("form-container");

    if (esFalso) {
        var sublabel= document.createElement("h1");
        sublabel.className="subtitle";
        sublabel.textContent="Solicitudes actuales";
        formContainer.appendChild(sublabel);

        var test = [["1","Aldo Cambronero","Jefe","Devel","Nacional","CR","500","19/5/2023","25/5/2023","Avianca","501","XD","si","Pendiente"], 
        ["2","Aldo Cambronero","Jefe","Devel","Nacional","CR","500","19/5/2023","25/5/2023","Avianca","501","XD","si","Pendiente"],
        ["3","Aldo Cambronero","Jefe","Devel","Nacional","CR","500","19/5/2023","25/5/2023","Avianca","501","XD","si","Pendiente"]];

        var table = document.createElement("table");
        table.className = "data-table";

        // Crea la fila de encabezados de la tabla
        var headerRow = document.createElement("tr");
        ["ID", "Nombre completo", "Puesto", "Departamento", "Internacional", "País de destino", "Motivo del viaje", "Inicio", "Finalización", "Aerolínea", "Precio", "Alojamiento", "Transporte", "Estado", "Proceso"].forEach(function(headerText) {
            var headerCell = document.createElement("th");
            headerCell.textContent = headerText;
            // Aplica estilos CSS a las celdas de encabezado
            headerCell.style.backgroundColor = "lightblue"; // Cambia el color de fondo
            headerCell.style.color = "black"; // Cambia el color del texto


            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);

        // Itera sobre los datos y crea filas de tabla
        test.forEach(function(rowData) {
            var row = document.createElement("tr");

            // Muestra el primer valor de cada sublista de test
            var firstValueCell = document.createElement("td");
            firstValueCell.textContent = rowData[0];
            row.appendChild(firstValueCell);

            // Muestra otros valores de la sublista
            for (var i = 1; i < rowData.length; i++) {
                var cell = document.createElement("td");
                cell.textContent = rowData[i];
                row.appendChild(cell);
            }

            // Agrega botones Aceptar y Rechazar
            var actionsCell = document.createElement("td");
            var acceptButton = document.createElement("button");
            acceptButton.textContent = "Aceptar";
            acceptButton.className = "action-button";
            acceptButton.addEventListener("click", function() {
                // Lógica para aceptar el viaje
                console.log("Viaje Aceptado: " + rowData[0]);
            });
            var rejectButton = document.createElement("button");
            rejectButton.textContent = "Rechazar";
            rejectButton.className = "action-button";
            rejectButton.addEventListener("click", function() {
                // Lógica para rechazar el viaje
                console.log("Viaje Rechazado: " + rowData[0]);
            });
            actionsCell.appendChild(acceptButton);
            actionsCell.appendChild(rejectButton);
            row.appendChild(actionsCell);

            table.appendChild(row);
        });
        formContainer.appendChild(table);
    }else {
        var message = document.createElement("h1");
        message.textContent = "No hay ninguna solicitud";
        formContainer.appendChild(message);
    }
};

