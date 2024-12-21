import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

import cv2 
from pyzbar.pyzbar import decode
import numpy as np


class ScannerService:
    def scan_and_fetch_product(self):
       
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while cap.isOpened():
            success, frame = cap.read()
            
            frame = cv2.flip(frame, 1)

            detectedBarcode = decode(frame)

            for barcode in detectedBarcode:
                if barcode.data: 
                    
                    barcode = barcode.data.decode('utf-8') if isinstance(barcode.data, bytes) else int(barcode.data)
                    cap.release()
                    cv2.destroyAllWindows()
                    print("BARCODE FOUND: ", barcode)
                    return int(barcode)
                
                    
            cv2.imshow('scanner', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return None










