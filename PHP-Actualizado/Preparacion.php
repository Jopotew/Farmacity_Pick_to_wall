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

// Obtener los artículos por orden (id_order_assign) desde la tabla `order_wave` y `items`
$sql = "SELECT items.*, order_wave.id_order_assign, order_wave.item_status 
        FROM order_wave 
        JOIN items ON order_wave.id_item = items.id_item
        JOIN order_assign ON order_wave.id_order_assign = order_assign.id_order_assign
        WHERE order_assign.id_status = 1"; // Solo artículos con status 1 (en preparación)

$result = $conn->query($sql);

$articulosPorOrden = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $id_order_assign = $row['id_order_assign'];
        // Obtener solo la primera palabra del nombre del artículo
        $primeraPalabra = explode(' ', trim($row['item_name']))[0];
        // Agrupar los ítems por id_order_assign
        if (!isset($articulosPorOrden[$id_order_assign])) {
            $articulosPorOrden[$id_order_assign] = []; // Crear un array vacío para la orden si no existe
        }
        // Agregar el ítem al array de la orden correspondiente
        $articulosPorOrden[$id_order_assign][] = [
            'nombre' => $primeraPalabra,
            'datos_completos' => $row // Guardar todos los datos del ítem
        ];
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
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 12px;
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
        .articulo {
            font-size: 10px;
            margin: 2px 0;
            text-align: center;
        }
        .verificado {
            color: green; /* Color verde para ítems verificados */
            font-weight: bold; /* Texto en negrita */
        }
        .no-verificado {
            color: red; /* Color rojo para ítems no verificados */
            font-weight: bold; /* Texto en negrita */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Preparación</h1>
        <div class="info">Cantidad de Pedidos restantes: <?php echo count($articulosPorOrden); ?></div>
        <div class="d-flex justify-content-center">
            <div id="tablero" class="d-flex flex-wrap" style="max-width: <?php echo $columnas * 110; ?>px;">
                <?php
                $contadorPosiciones = 0;
                $totalPosiciones = $filas * $columnas; // Total de posiciones en el tablero
                foreach ($articulosPorOrden as $id_order_assign => $articulos) {
                    if ($contadorPosiciones >= $totalPosiciones) {
                        break; // No exceder el tamaño del tablero
                    }
                    $contadorPosiciones++;
                    $posicion = $contadorPosiciones;
                    if (in_array((string)$posicion, $posicionesInhabilitadas)) {
                        echo "<div class='casillero disabled'>X</div>";
                    } else {
                        echo "<div class='casillero'>";
                        echo "<strong>Orden: $id_order_assign</strong>";
                        foreach ($articulos as $articulo) {
                            // Convertir el nombre del ítem a un ID válido
                            $idItem = str_replace(' ', '-', strtolower($articulo['nombre']));
                            // Verificar si el ítem está verificado o no
                            $claseVerificado = $articulo['datos_completos']['item_status'] == 1 ? 'verificado' : 'no-verificado';
                            echo "<div id='$idItem' class='articulo $claseVerificado'>{$articulo['nombre']}</div>";
                        }
                        echo "</div>";
                    }
                }
                // Rellenar las posiciones restantes del tablero
                for ($i = $contadorPosiciones + 1; $i <= $totalPosiciones; $i++) {
                    if (in_array((string)$i, $posicionesInhabilitadas)) {
                        echo "<div class='casillero disabled'>X</div>";
                    } else {
                        echo "<div class='casillero'></div>";
                    }
                }
                ?>
            </div>
        </div>
        <div class="mt-4">
            <button class="btn-custom" onclick="location.href='inicio.html'">Cancelar Ola</button>
            <button class="btn-custom" onclick="location.href='OlaCompletada.html'">Finalizar</button>
        </div>
    </div>

    <!-- Bootstrap JS y dependencias -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>

    <script>
        // Refrescar la página cada 10 segundos (10000 ms)
        setTimeout(() => {
            window.location.reload();
        }, 10000);
    </script>
</body>
</html>
