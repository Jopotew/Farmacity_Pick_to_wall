<?php
// Incluido en CONFIGURAR_TABLERO. Lo dejo como respaldo.

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

// Obtener las posiciones inhabilitadas desde la tabla `posicion`
$sqlPosiciones = "SELECT posicion FROM posicion WHERE habilitada = 0";
$resultPosiciones = $conn->query($sqlPosiciones);

$posicionesInhabilitadas = [];
if ($resultPosiciones->num_rows > 0) {
    while ($row = $resultPosiciones->fetch_assoc()) {
        // Convertir formato 'fila-columna' a número de casillero
        list($fila, $columna) = explode("-", $row['posicion']);
        $posicionId = ($fila - 1) * $columnas + $columna;
        $posicionesInhabilitadas[] = $posicionId;
    }
}

$conn->close();

// Guardar configuración si se envió el formulario
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $filas = (int) $_POST["filas"];
    $columnas = (int) $_POST["columnas"];
    $posicionesInhabilitadas = isset($_POST["posiciones_inhabilitadas"]) ? explode(",", $_POST["posiciones_inhabilitadas"]) : [];

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }

    // Actualizar filas y columnas en `configuracion`
    $sql1 = "UPDATE configuracion SET valor_parametro = $filas WHERE nombre_parametro = 'cantfila'";
    $sql2 = "UPDATE configuracion SET valor_parametro = $columnas WHERE nombre_parametro = 'cantcol'";

    // Ejecutar las consultas para actualizar filas y columnas
    if ($conn->query($sql1) === TRUE && $conn->query($sql2) === TRUE) {
        // Eliminar todas las posiciones existentes en la tabla `posicion`
        $sqlDelete = "DELETE FROM posicion";
        if ($conn->query($sqlDelete) === TRUE) {
            // Insertar todas las posiciones (habilitadas e inhabilitadas)
            for ($i = 1; $i <= $filas; $i++) {
                for ($j = 1; $j <= $columnas; $j++) {
                    $posicion = "$i-$j"; // Formato 'fila-columna'
                    $habilitada = in_array(($i - 1) * $columnas + $j, $posicionesInhabilitadas) ? 0 : 1;

                    // Insertar la posición en la tabla `posicion`
                    $sqlInsert = "INSERT INTO posicion (posicion, habilitada) VALUES ('$posicion', $habilitada)";
                    $conn->query($sqlInsert);
                }
            }

            header("Location: inicio.html"); // Redirigir al inicio después de guardar
            exit;
        } else {
            $mensaje = "Error al eliminar las posiciones antiguas: " . $conn->error;
        }
    } else {
        $mensaje = "Error al guardar la configuración: " . $conn->error;
    }

    $conn->close();
}
?>