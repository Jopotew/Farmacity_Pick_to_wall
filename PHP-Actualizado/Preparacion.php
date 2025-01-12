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

// Obtener las filas y columnas del tablero desde la tabla `grid`
$sql = "SELECT gridcol, gridrow, pos_unab FROM grid WHERE id_grid = 1";
$result = $conn->query($sql);

// Obtener las filas y columnas por defecto 
$filas = 3;
$columnas = 3;
$posicionesInhabilitadas = [];

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $filas = (int) $row["gridrow"];
    $columnas = (int) $row["gridcol"];
    $posicionesInhabilitadas = $row["pos_unab"] ? explode(",", $row["pos_unab"]) : [];
}
// REVISAR: por las posiciones inhabilitadas, lógica de BD para tapar casillas.
// Obtener los artículos por posición desde la tabla `order_wave` y `items`
$sql = "SELECT items.item_name, order_wave.id_order_assign 
        FROM order_wave 
        JOIN items ON order_wave.id_item = items.id_item";
$result = $conn->query($sql);

$articulos = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $articulos[] = $row['item_name'];
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preparación</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #00a339; 
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        h1 {
            margin-top: 20px;
        }
        .casillero {
            background-color: white;
            border: 2px solid black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: black;
            height: 100px;
            width: 100px;
            margin: 5px;
            padding: 5px;
            overflow: hidden;
            word-wrap: break-word;
            white-space: normal;
            text-overflow: ellipsis;
        }
        .casillero.disabled {
            background-color: #000000;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center; 
            font-size: 40px;
            font-weight: bold;
        }
        .btn-custom {
            background-color: #eb7100; 
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            margin: 10px;
        }
        .btn-custom:hover {
            background-color: #ff8c00; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Preparación</h1>
        <div class="info">Cantidad de Pedidos restantes: <?php echo count($articulos); ?></div>
        <div class="d-flex justify-content-center">
            <div id="tablero" class="d-flex flex-wrap" style="max-width: <?php echo $columnas * 110; ?>px;">
                <?php
                $contadorArticulos = 0;
                for ($i = 1; $i <= $filas; $i++) {
                    for ($j = 1; $j <= $columnas; $j++) {
                        $posicion = ($i-1) * $columnas + $j;
                        if (in_array((string)$posicion, $posicionesInhabilitadas)) {
                            echo "<div class='casillero disabled'>X</div>";
                        } else {
                            $articulo = isset($articulos[$contadorArticulos]) ? $articulos[$contadorArticulos] : '';
                            echo "<div class='casillero'>$articulo</div>";
                            $contadorArticulos++;
                        }
                    }
                }
                ?>
            </div>
        </div>
        <div class="mt-4">
            <button class="btn-custom" onclick="location.href='inicio.html'">Cancelar Ola</button>
             <!-- Revisar funcionalidad del botón "BOTÓN" -->
            <button class="btn-custom" onclick="location.href='OlaCompletada.html'">Botón</button>
        </div>
    </div>

    <!-- Bootstrap JS y dependencias -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
</body>
</html>