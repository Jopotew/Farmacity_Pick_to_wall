import RPi.GPIO as GPIO
import time

# Configuración del modo de numeración de pines
GPIO.setmode(GPIO.BCM)  # Usar la numeración BCM de la placa

# Configuración del pin GPIO 21 como salida
GPIO.setup(21, GPIO.OUT)

try:
    while True:
        # Encender el LED
        GPIO.output(21, GPIO.HIGH)
        time.sleep(1)  # Esperar 1 segundo
        
        # Apagar el LED
        GPIO.output(21, GPIO.LOW)
        time.sleep(1)  # Esperar 1 segundo

except KeyboardInterrupt:
    # Limpiar GPIO al salir
    GPIO.cleanup()
    print("Programa terminado y GPIO limpiado.")


#sudo python3 /home/agus/share/raspberry_LED.py para poder correrlo.

