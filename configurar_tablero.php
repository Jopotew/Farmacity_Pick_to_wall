<?php
// Conexión a la base de datos
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "trabajofarmacity";

$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Valores predeterminados
$filas = 3;
$columnas = 3;

// Obtener los valores almacenados en la base de datos
$sql = "SELECT valor_parametro, nombre_parametro FROM configuracion WHERE nombre_parametro IN ('cantfila', 'cantcol')";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        if ($row["nombre_parametro"] == "cantfila") {
            $filas = (int) $row["valor_parametro"];
        } elseif ($row["nombre_parametro"] == "cantcol") {
            $columnas = (int) $row["valor_parametro"];
        }
    }
}

$conn->close();

// Guardar configuración si se envió el formulario
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $filas = (int) $_POST["filas"];
    $columnas = (int) $_POST["columnas"];

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }

    $sql1 = "UPDATE configuracion SET valor_parametro = $filas WHERE nombre_parametro = 'cantfila'";
    $sql2 = "UPDATE configuracion SET valor_parametro = $columnas WHERE nombre_parametro = 'cantcol'";

    if ($conn->query($sql1) === TRUE && $conn->query($sql2) === TRUE) {
        header("Location: inicio.html"); // Redirigir al inicio después de guardar
        exit;
    } else {
        $mensaje = "Error al guardar la configuración.";
    }

    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configurar Tablero</title>
    <style>
        /* Estilos del tablero */
        #tablero {
            display: grid;
            margin-top: 20px;
            border: 2px solid black;
            grid-gap: 1px;
        }
        .casillero {
            width: 40px;
            height: 40px;
            background-color: white;
            border: 1px solid black;
        }
    </style>
</head>
<body>
<div id="configurar-tablero" style="text-align: center; margin-top: 5%;">
    <h1>Configurar Tablero</h1>
    <?php if (!empty($mensaje)) : ?>
        <p style="color: red;"><?php echo $mensaje; ?></p>
    <?php endif; ?>
    <form method="POST">
        <div>
            <label for="filas">Cantidad de filas:</label>
            <input type="number" id="filas" name="filas" value="<?php echo $filas; ?>" min="1" onchange="actualizarTablero()">
        </div>
        <div>
            <label for="columnas">Cantidad de columnas:</label>
            <input type="number" id="columnas" name="columnas" value="<?php echo $columnas; ?>" min="1" onchange="actualizarTablero()">
        </div>
        <div id="tablero"></div>
        <p>Total de casilleros disponibles: <span id="total-casilleros"><?php echo $filas * $columnas; ?></span></p>
        <div>
            <button type="button" onclick="location.href='inicio.html'" style="margin-right: 10px;">Volver al Inicio</button>
            <button type="submit">Guardar Configuración</button>
        </div>
    </form>
</div>

<script>
// Función para actualizar el tablero en tiempo real
function actualizarTablero() {
    const filas = document.getElementById('filas').value;
    const columnas = document.getElementById('columnas').value;
    const totalCasilleros = filas * columnas;
    const tablero = document.getElementById('tablero');
    const totalCasillerosSpan = document.getElementById('total-casilleros');

    // Actualizar el número total de casilleros
    totalCasillerosSpan.textContent = totalCasilleros;

    // Configurar el estilo del tablero
    tablero.style.gridTemplateRows = `repeat(${filas}, 40px)`;
    tablero.style.gridTemplateColumns = `repeat(${columnas}, 40px)`;

    // Limpiar y crear casilleros
    tablero.innerHTML = '';
    for (let i = 0; i < totalCasilleros; i++) {
        const casillero = document.createElement('div');
        casillero.classList.add('casillero');
        tablero.appendChild(casillero);
    }
}

// Llamar a la función de actualización al cargar la página
window.onload = actualizarTablero;
</script>
</body>
</html>