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

// Obtener los valores de filas y columnas desde la URL
$filas = $_GET['filas'];
$columnas = $_GET['columnas'];

// Actualizar los valores en la base de datos
$sqlFilas = "UPDATE configuracion SET valor_parametro = '$filas' WHERE nombre_parametro = 'cantfila'";
$sqlColumnas = "UPDATE configuracion SET valor_parametro = '$columnas' WHERE nombre_parametro = 'cantcol'";

// Ejecutar las consultas
$successFilas = $conn->query($sqlFilas);
$successColumnas = $conn->query($sqlColumnas);

// Verificar si las actualizaciones fueron exitosas
if ($successFilas && $successColumnas) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false]);
}

$conn->close();
?>