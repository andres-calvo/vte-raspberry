import RPi.GPIO as GPIO
import time
import io
import pynmea2
import serial
import threading

# Configuracion serial GPS
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# Configuración de los pines
HALL_SENSOR_PIN = 17  # GPIO para el sensor de efecto Hall
TRIG_PIN = 22         # GPIO para el pin Trigger del sensor ultrasónico
ECHO_PIN = 23         # GPIO para el pin Echo del sensor ultrasónico

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)  # Usar la numeración de pines BCM
GPIO.setup(HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Variables globales
pulse_count = 0
last_time = 0
wheel_circumference = 0.1256637061  # Circunferencia de la rueda delantera en metros
speed = 0  # Velocidad en m/s
lat = 0
lng = 0

# Función para medir la distancia con el sensor ultrasónico
def medir_distancia():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.02)  

    # Enviar un pulso de 10 microsegundos al pin Trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Esperar la señal de Echo
    while GPIO.input(ECHO_PIN) == 0:
        inicio = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        fin = time.time()
    
    # Calcular la distancia
    duracion = fin - inicio
    distancia = duracion * 17150  # Convertir a cm
    return round(distancia, 2)

# Función de interrupción que cuenta los pulsos del sensor de efecto Hall
def count_pulse(channel):
    global pulse_count, last_time, speed
    pulse_count += 1
    current_time = time.time()
    
    if pulse_count > 0:
        # Calcular el tiempo transcurrido desde el último pulso
        time_elapsed = (current_time - last_time) * 1000  # Convertir a ms
        
        # Calcular la velocidad (velocidad = distancia / tiempo)
        speed = (wheel_circumference / time_elapsed) * 1000  # Convertir a m/s
        
        # Actualizar el tiempo del último pulso
        last_time = current_time

# Configurar interrupción para el sensor de efecto Hall
GPIO.add_event_detect(HALL_SENSOR_PIN, GPIO.FALLING, callback=count_pulse)

def gps():
    global lat, lng
    while True:
        try:
            line = sio.readline()
            msg = pynmea2.parse(line)
            if(hasattr(msg, 'latitude ') and hasattr(msg, 'longitude ')):
                lat = msg.latitude 
                lng = msg.longitude
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            break
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue    
    

def main():
    try:
        gps_thread = threading.Thread(target=gps)
        gps_thread.start()
        while True:
            distancia_ultrasonico = medir_distancia()
            print(f"Distancia medida: {distancia_ultrasonico} cm")
    
            
            if pulse_count > 0:
                print(f"Velocidad: {speed:.2f} m/s")
                pulse_count = 0  

            ##Send to db heere
            
            time.sleep(0.5) 
    except KeyboardInterrupt:
        print("Programa finalizado.")
    finally:
        GPIO.cleanup()
    
    



if __name__ == '__main__':
    main()