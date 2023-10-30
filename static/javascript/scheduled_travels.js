const socket = io.connect('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to server, travel request --------');
});

window.onload = function() {
    var esFalso = true; // Cambiar a true o false según sea necesario
    var formContainer = document.getElementById("form-container");

    //Hay que sacar los valores de la base de datos, aqui esta un ejemplo basico

    if (esFalso) {
        var test = 
        [["Aldo Cambronero","Devel"], 
        ["Aldo Cambronero","Devel"],
        ["Aldo Cambronero","Devel"]];

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
        test.forEach(function(rowData) {
            var row = document.createElement("tr");
            rowData.forEach(function(cellData) {
                var cell = document.createElement("td");
                cell.textContent = cellData;
                row.appendChild(cell);
            });
            table.appendChild(row);
        });

        formContainer.appendChild(table);
    } else {
        var message = document.createElement("h1");
        message.textContent = "No posee ningún registro asociado";
        formContainer.appendChild(message);
    }
};