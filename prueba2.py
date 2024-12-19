import cv2
from pyzbar.pyzbar import decode
import mysql.connector
from mysql.connector import Error

def scan_and_fetch_product():
    try:
        conexion = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='farmacity',
            port='3306'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

    cur = conexion.cursor()
    consulta = "SELECT * FROM productos WHERE codigo_barras = %s"

    # Lector de imagen
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        
        frame = cv2.flip(frame, 1)

        detectedBarcode = decode(frame)

        for barcode in detectedBarcode:
            if barcode.data: 
                
                barcode_str = barcode.data.decode('utf-8') if isinstance(barcode.data, bytes) else str(barcode.data)
                
                try:
                    cur.execute(consulta, (barcode_str,))
                    resultado = cur.fetchone()
                    
                    if resultado:
                        print(f"Producto encontrado: {resultado}")
                        cap.release()
                        cv2.destroyAllWindows()
                        return resultado 
                    else:
                        print("No se encontró ningún producto con ese código de barras.")
                except Error as e:
                    print(f"Error al ejecutar la consulta SQL: {e}")

        cv2.imshow('scanner', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    producto = scan_and_fetch_product()
    if producto:
        print("Producto obtenido:", producto)
    else:
        print("No se obtuvo ningún producto.")
