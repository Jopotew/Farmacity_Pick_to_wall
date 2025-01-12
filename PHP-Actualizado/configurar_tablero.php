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

// Valores predeterminados para filas, columnas y posiciones inhabilitadas
$filas = 3;
$columnas = 3;
$posicionesInhabilitadas = [];

// REVISAR: si conviene agregar a la base de datos una tabla para todas las posiciones inhabilitadas.
// Obtener los valores almacenados en la tabla grid
$sql = "SELECT * FROM grid WHERE id_grid = 1";
$result = $conn->query($sql);

if ($result->num_rows == 0) {
    // Si no existe ningún registro, crear uno por defecto
    $sql = "INSERT INTO grid (gridcol, gridrow, pos_unab) VALUES (3, 3, NULL)";
    $conn->query($sql);
    $filas = 3;
    $columnas = 3;
    $posicionesInhabilitadas = [];
} else {
    // Usar la configuración existente
    $row = $result->fetch_assoc();
    $filas = (int) $row["gridrow"];
    $columnas = (int) $row["gridcol"];
    $posicionesInhabilitadas = $row["pos_unab"] ? explode(",", $row["pos_unab"]) : [];
}

// Guardar configuración si se envió el formulario
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $filas = (int) $_POST["filas"];
    $columnas = (int) $_POST["columnas"];
    $posicionesInhabilitadas = isset($_POST["posiciones_inhabilitadas"]) ? 
        array_filter(explode(",", $_POST["posiciones_inhabilitadas"])) : [];
    
    $pos_unab = !empty($posicionesInhabilitadas) ? implode(",", $posicionesInhabilitadas) : NULL;

    // Actualizar o insertar en la tabla grid
    $sql = "INSERT INTO grid (id_grid, gridcol, gridrow, pos_unab) 
            VALUES (1, $columnas, $filas, " . ($pos_unab ? "'$pos_unab'" : "NULL") . ")
            ON DUPLICATE KEY UPDATE 
            gridcol = VALUES(gridcol),
            gridrow = VALUES(gridrow),
            pos_unab = VALUES(pos_unab)";

    if ($conn->query($sql) === TRUE) {
        header("Location: inicio.html");
        exit;
    } else {
        $mensaje = "Error al guardar la configuración: " . $conn->error;
    }
}

$conn->close();

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configurar Tablero</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Estilos personalizados para Farmacity con verde */
        body {
            background-color: #f8f9fa; /* Color de fondo suave */
        }
        .farmacity-primary {
            background-color: #28a745; /* Verde de Farmacity */
            color: white;
        }
        .farmacity-secondary {
            background-color: #6c757d; /* Gris de Farmacity */
            color: white;
        }
        .btn-naranja {
            background-color: #ff8c00; /* Naranja */
            color: white;
            border: none;
        }
        .btn-naranja:hover {
            background-color: #e07b00; /* Naranja más oscuro al pasar el mouse */
        }
        .casillero {
            width: 40px;
            height: 40px;
            background-color: white;
            border: 1px solid #28a745; /* Borde verde */
            cursor: pointer;
        }
        .casillero.disabled {
            background-color: #514b4f; /* Color para casilleros inhabilitados */
            color: white;
        }
        #tablero {
            display: grid;
            margin-top: 20px;
            border: 2px solid #28a745; /* Borde verde */
            grid-gap: 1px;
        }
    </style>
</head>
<body>
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header farmacity-primary">
                    <h1 class="card-title text-center">Configurar Tablero</h1>
                </div>
                <div class="card-body">
                    <?php if (!empty($mensaje)) : ?>
                        <div class="alert alert-danger"><?php echo $mensaje; ?></div>
                    <?php endif; ?>
                    <form method="POST">
                        <div class="mb-3">
                            <label for="filas" class="form-label">Cantidad de filas:</label>
                            <input type="number" class="form-control" id="filas" name="filas" value="<?php echo $filas; ?>" min="1" onchange="actualizarTablero()">
                        </div>
                        <div class="mb-3">
                            <label for="columnas" class="form-label">Cantidad de columnas:</label>
                            <input type="number" class="form-control" id="columnas" name="columnas" value="<?php echo $columnas; ?>" min="1" onchange="actualizarTablero()">
                        </div>
                        <div id="tablero" class="mb-3"></div>
                        <p class="text-center">Total de casilleros disponibles: <span id="total-casilleros"><?php echo $filas * $columnas; ?></span></p>
                        <p class="text-center">Posiciones inhabilitadas: <span id="posiciones-inhabilitadas-display"><?php echo implode(", ", $posicionesInhabilitadas); ?></span></p>
                        <input type="hidden" id="posiciones-inhabilitadas" name="posiciones_inhabilitadas" value="<?php echo implode(",", $posicionesInhabilitadas); ?>">
                        <div class="d-grid gap-2">
                            <button type="button" class="btn btn-naranja" onclick="location.href='inicio.html'">Volver al Inicio</button>
                            <button type="submit" class="btn farmacity-primary">Guardar Configuración</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Bootstrap JS y dependencias -->
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>

<script>
// Función para actualizar el tablero en tiempo real
function actualizarTablero() {
    const filas = document.getElementById('filas').value;
    const columnas = document.getElementById('columnas').value;
    const totalCasilleros = filas * columnas;
    const tablero = document.getElementById('tablero');
    const totalCasillerosSpan = document.getElementById('total-casilleros');
    const posicionesInhabilitadas = document.getElementById('posiciones-inhabilitadas').value.split(",");

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
        casillero.textContent = i + 1;

        // Marcar casilleros inhabilitados
        if (posicionesInhabilitadas.includes((i + 1).toString())) {
            casillero.classList.add('disabled');
        }

        // Evento para marcar/desmarcar casilleros
        casillero.addEventListener('click', () => {
            toggleCasillero(casillero, i + 1);
        });

        tablero.appendChild(casillero);
    }
}

// Función para marcar/desmarcar casilleros
function toggleCasillero(casillero, numeroCasillero) {
    const posicionesInhabilitadasInput = document.getElementById('posiciones-inhabilitadas');
    // Asegurarse de que posicionesInhabilitadas sea un array, incluso si está vacío
    let posicionesInhabilitadas = posicionesInhabilitadasInput.value ? 
        posicionesInhabilitadasInput.value.split(",").filter(Boolean) : [];

    if (casillero.classList.contains('disabled')) {
        // Remover posición
        casillero.classList.remove('disabled');
        posicionesInhabilitadas = posicionesInhabilitadas.filter(pos => pos !== numeroCasillero.toString());
    } else {
        // Agregar posición
        casillero.classList.add('disabled');
        if (!posicionesInhabilitadas.includes(numeroCasillero.toString())) {
            posicionesInhabilitadas.push(numeroCasillero.toString());
        }
    }

    // Ordenar las posiciones numéricamente
    posicionesInhabilitadas.sort((a, b) => parseInt(a) - parseInt(b));
    
    // Actualizar el campo oculto
    posicionesInhabilitadasInput.value = posicionesInhabilitadas.join(",");

    // Actualizar el display
    const filas = parseInt(document.getElementById('filas').value);
    const columnas = parseInt(document.getElementById('columnas').value);
    
    const posicionesFormateadas = posicionesInhabilitadas.map(pos => {
        const posicionNum = parseInt(pos, 10);
        const fila = Math.ceil(posicionNum / columnas);
        const columna = (posicionNum % columnas === 0) ? columnas : posicionNum % columnas;
        return `${fila}-${columna}`;
    });

    document.getElementById('posiciones-inhabilitadas-display').textContent = 
        posicionesFormateadas.length > 0 ? posicionesFormateadas.join(", ") : "Ninguna";
}

// Llamar a la función de actualización al cargar la página
window.onload = actualizarTablero;
</script>
</body>
</html>