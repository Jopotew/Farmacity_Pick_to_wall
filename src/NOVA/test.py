import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)
import cv2
from services.order_service import OrderService
from pyzbar.pyzbar import decode
from PIL import Image
import imageio.v3 as iio

def scan_and_fetch_product():
   

    # Lector de imagen
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():
        success, frame = cap.read()
        
        frame = cv2.flip(frame, 1)

        detectedBarcode = decode(frame)

        for barcode in detectedBarcode:
            if barcode.data: 
                
                barcode_str = barcode.data.decode('utf-8') if isinstance(barcode.data, bytes) else str(barcode.data)
                cap.release()
                cv2.destroyAllWindows()
                print(barcode_str)
                return barcode_str 
              
                
        cv2.imshow('scanner', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None



# Ejemplo de uso
if __name__ == "__main__":

    # list_cameras()
    # check_camera()

    

    barcode = scan_and_fetch_product()
    order_service = OrderService()

    sorted_orders = order_service.get_orders()
    print(barcode)
    try:
        if barcode:
            print(f"Código de barras detectado: {barcode}")
            # Aquí puedes llamar a tu función para buscar el producto con el código de barras
            product = order_service.search_by_barcode(
                sorted_orders, barcode
            )  # Reemplaza con tu función
            if product:
                print("Producto encontrado:", product)
            else:
                print("No se encontró ningún producto con ese código de barras.")
        else:
            print("No se detectó ningún código de barras.")
    finally:
        pass
