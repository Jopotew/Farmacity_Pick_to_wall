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

// Obtener las filas y columnas del tablero desde la base de datos
$sql = "SELECT valor_parametro, nombre_parametro FROM configuracion WHERE nombre_parametro IN ('cantfila', 'cantcol')";
$result = $conn->query($sql);

$filas = 3;
$columnas = 3;

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        if ($row["nombre_parametro"] == "cantfila") {
            $filas = (int) $row["valor_parametro"];
        } elseif ($row["nombre_parametro"] == "cantcol") {
            $columnas = (int) $row["valor_parametro"];
        }
    }
}

// Obtener los artículos por posición desde la tabla olapreparacion //////////
$sql = "SELECT * FROM olapreparacion";
$result = $conn->query($sql);

$articulos = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $posicion = explode('-', $row['posicion']);
        $fila = (int) $posicion[0];
        $columna = (int) $posicion[1];
        $articulos[$fila][$columna] = $row['articulo'];
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
    <style>
        body {
            background-color: #006400; /* Verde oscuro */
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        h1 {
            margin-top: 20px;
        }
        #tablero {
            display: grid;
            grid-template-rows: repeat(<?php echo $filas; ?>, 100px);
            grid-template-columns: repeat(<?php echo $columnas; ?>, 100px);
            grid-gap: 10px;
            justify-content: center;
            margin: 20px auto;
            width: max-content;
        }
        .casillero {
            background-color: white;
            border: 2px solid black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: black;
        }
        .icon {
            font-size: 40px;
        }
        .info {
            margin: 10px;
            font-size: 18px;
        }
        button {
            background-color: white;
            color: black;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 20px;
            margin: 10px;
            cursor: pointer;
        }
        button:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <h1>Preparación</h1>
    <div class="info">Cantidad de Pedidos restantes: 2</div>
    <div id="tablero">
    <!-- Esto hay que revisar por lo del Figma! -->
        <?php
        for ($i = 1; $i <= $filas; $i++) {
            for ($j = 1; $j <= $columnas; $j++) {
                $articulo = isset($articulos[$i][$j]) ? $articulos[$i][$j] : '';
                $icono = '';
                // Simular diferentes iconos
                if ($articulo == 'alerta') {
                    $icono = "&#9888;"; // Alerta ⚠
                } elseif ($articulo == 'bolsa') {
                    $icono = "&#128092;"; // Bolsa 👜
                } elseif ($articulo == 'caja') {
                    $icono = "&#128230;"; // Caja 📦
                }
                echo "<div class='casillero'><span class='icon'>$icono</span></div>";
            }
        }
        ?>
    </div>
    <button onclick="location.href='inicio.html'">Cancelar Ola</button>
    <button onclick="alert('Funcionalidad pendiente')">Botón</button>
</body>
</html>
