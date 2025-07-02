from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import Image, ImageFont, ImageDraw, ImageOps
import socket
import threading
import pyaudio
import time
import numpy as np
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from pydub import AudioSegment
from pydub.playback import play
import io
import select

# ---- Configuración de la cámara ----
picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(video_config)
picam2.set_controls({"AwbMode": 3})  # 3 = luz del día
picam2.start()

# ---- Configuración del servo ----
SERVO_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz
pwm.start(0)

# ---- Configuración OLED ----
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Lock para acceso thread-safe al display
display_lock = threading.Lock()

# Configuración de fuente
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except IOError:
    font = ImageFont.load_default()

# ---- Configuración UDP ----
UDP_IP_PC = "192.168.7.1"  # IP de PC
UDP_OPEN = '0.0.0.0'

# Puertos para diferentes servicios
UDP_PORT_CAM = 5002        # Puerto para enviar video
UDP_PORT_SERVO = 5001      # Puerto para recibir comandos de servo
UDP_PORT_MICROFONO = 5006   # Puerto para enviar audio al PC
UDP_PORT_TEXT = 5005       # Puerto para recibir transcripciones
UDP_PORT_PARLANTE = 5003   # Puerto para recibir audio del PC

#NEUVO Agregar nuevo puerto
UDP_PORT_HANDS_STATUS = 5007
hands_status_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hands_status_sock.bind((UDP_OPEN, UDP_PORT_HANDS_STATUS))
hands_status_sock.setblocking(False)

# ---- Agregar nuevo puerto y variables ----
UDP_PORT_HEARTBEAT = 5008
heartbeat_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
heartbeat_sock.bind((UDP_OPEN, UDP_PORT_HEARTBEAT))
heartbeat_sock.setblocking(False)

# Variables para control de timeout
last_heartbeat_time = time.time()
HEARTBEAT_TIMEOUT = 3  # 3 segundos sin heartbeat = motor apagado

# Tamaño máximo del fragmento UDP
MAX_FRAGMENT_SIZE = 1460

# Buffer UDP
BUFFER_UDP = 65536 #16 bits

# Crear sockets
video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_UDP)

command_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
text_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Configurar sockets de recepción
command_sock.bind((UDP_OPEN, UDP_PORT_SERVO))
text_sock.bind((UDP_OPEN, UDP_PORT_TEXT))
audio_rx_sock.bind((UDP_OPEN, UDP_PORT_PARLANTE))

# Configurar sockets no bloqueantes
command_sock.setblocking(False)
audio_rx_sock.setblocking(False)
text_sock.setblocking(False)

# ---- Configuración de audio ----
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 48000
CHUNK = 1024

# Parámetros de audio y control
audio_buffer = bytearray()
last_audio_time = 0
AUDIO_TIMEOUT = 0.5  # 500 ms

# ---- Parámetros de control del servo ----
CENTER_ANGLE = 90  # Posición central
MIN_ANGLE = 0      # Límite inferior
MAX_ANGLE = 180    # Límite superior
#NUEVOI
last_hand_detected = False

class ServoController:
    def __init__(self, initial_angle=90):
        self.current_angle = initial_angle
        #NEUVO
        self.last_update = 0
        self.motor_active = False  # Estado del motor (encendido/apagado)

    def toggle_motor(self, activate):
        """Activa/desactiva el motor según la detección de manos"""
        if activate != self.motor_active:
            if activate:
                pwm.start(0)  # Reactivar PWM
            else:
                pwm.ChangeDutyCycle(0)  # Detener el servo
            self.motor_active = activate#HASTACA

    def set_servo_angle(self, angle_change):
        """Establece el ángulo del servomotor"""
        """Mover solo si el motor está activo"""
        if self.motor_active and (time.time() - self.last_update > 0.1):  #NUEVO Filtro de 100ms
            new_angle = self.current_angle - angle_change
            new_angle = max(MIN_ANGLE, min(MAX_ANGLE, new_angle))
            
            duty = (new_angle / 18) + 2
            pwm.ChangeDutyCycle(duty)
            
            self.current_angle = new_angle
            #print(f"Current Angle: {self.current_angle}")
            self.last_update = time.time() #NUEVO
            return self.current_angle

def reinicializar_display():
    global serial, device
    try:
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        print("Display reinicializado correctamente")
    except Exception as e:
        print(f"Error al reinicializar display: {e}")

def mostrar_texto(texto):
    with display_lock:  # Aseguramos acceso exclusivo al display
        max_reintentos = 3
        for reintento in range(max_reintentos):
            try:
                image = Image.new('1', (device.width, device.height))
                draw = ImageDraw.Draw(image)

                # Procesamiento del texto
                lineas = []
                palabras = texto.split()
                linea_actual = ""
                for palabra in palabras:
                    bbox = draw.textbbox((0, 0), linea_actual + " " + palabra, font=font)
                    ancho_texto = bbox[2] - bbox[0]
                    if ancho_texto <= device.width:
                        linea_actual += " " + palabra
                    else:
                        lineas.append(linea_actual.strip())
                        linea_actual = palabra
                lineas.append(linea_actual.strip())

                y_text = 0
                for linea in lineas:
                    draw.text((0, y_text), linea, font=font, fill="white")
                    y_text += 16

                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                
                device.display(image)
                break  # Salir si tuvo éxito
            except OSError as e:
                print(f"Error de E/S (reintento {reintento + 1}/{max_reintentos}): {e}")
                reinicializar_display()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error inesperado: {e}")
                break

def enviar_audio():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=1,
        frames_per_buffer=CHUNK
    )
    
    print("Comenzando transmisión de audio...")
    try:
        while True:
            data = stream.read(CHUNK)
            audio_tx_sock.sendto(data, (UDP_IP_PC, UDP_PORT_MICROFONO))
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def play_audio(buffer):
    try:
        audio = AudioSegment.from_file(io.BytesIO(buffer), format="wav")
        play(audio)
    except Exception as e:
        print(f"Error de reproducción: {str(e)}")

def procesar_comandos():
    servo_controller = ServoController()
    global audio_buffer, last_audio_time
    global last_heartbeat_time
    
    try:
        while True:
            # Manejar sockets de entrada para comandos y audio
            rlist, _, _ = select.select([command_sock, audio_rx_sock, text_sock, hands_status_sock,heartbeat_sock], [], [], 0.1)
            
            for sock in rlist:
                if sock == command_sock:
                    # Manejar comando de servo
                    try:
                        command, addr = command_sock.recvfrom(1024)
                        servo_position = int(command.decode())
                        servo_controller.set_servo_angle(servo_position)
                    except (BlockingIOError, ValueError) as e:
                        pass
                        
                elif sock == audio_rx_sock:
                    # Recibir audio
                    try:
                        data, addr = audio_rx_sock.recvfrom(MAX_FRAGMENT_SIZE)
                        audio_buffer.extend(data)
                        last_audio_time = time.time()
                    except BlockingIOError:
                        pass
                
                elif sock == text_sock:
                    # Recibir transcripciones
                    try:
                        data, _ = text_sock.recvfrom(1024)
                        texto = data.decode()
                        print("Transcripción recibida:", texto)
                        mostrar_texto(texto)
                    except BlockingIOError:
                        pass
                #NUEVO  
                elif sock == hands_status_sock:
                    try:
                        data, _ = hands_status_sock.recvfrom(1024)
                        status = data.decode()
                        if status == "HANDS_DETECTED":
                            servo_controller.toggle_motor(True)
                        elif status == "NO_HANDS":
                            servo_controller.toggle_motor(False)
                    except BlockingIOError:
                        pass
                    
                    
                elif sock == heartbeat_sock:
                    try:
                        data, _ = heartbeat_sock.recvfrom(1024)
                        message = data.decode()
                        if message == "HEARTBEAT":
                            last_heartbeat_time = time.time()  # Actualizar tiempo
                        elif message == "PROGRAM_EXIT":
                            servo_controller.toggle_motor(False)  # Apagar motor inmediatamente
                    except BlockingIOError:
                        pass#HASTACA

            # Verificar timeout del heartbeat
            if time.time() - last_heartbeat_time > HEARTBEAT_TIMEOUT:
                servo_controller.toggle_motor(False)
            
            # Manejar reproducción de audio
            if audio_buffer and (time.time() - last_audio_time > AUDIO_TIMEOUT):
                # Crear hilo de reproducción
                buffer_copy = bytes(audio_buffer)
                threading.Thread(target=play_audio, args=(buffer_copy,), daemon=True).start()
                audio_buffer.clear()
                
    except Exception as e:
        print(f"Error en procesamiento de comandos: {e}")

def transmitir_video():
    try:
        while True:
            # Capturar y enviar video
            frame = picam2.capture_array("main")
            _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            frame_bytes = encoded_frame.tobytes()
            
            num_fragments = (len(frame_bytes) + MAX_FRAGMENT_SIZE - 1) // MAX_FRAGMENT_SIZE
            for i in range(num_fragments):
                start = i * MAX_FRAGMENT_SIZE
                end = start + MAX_FRAGMENT_SIZE
                video_sock.sendto(frame_bytes[start:end], (UDP_IP_PC, UDP_PORT_CAM))
            
            time.sleep(0.04)  # Controlar tasa de frames (25 FPS)
    except Exception as e:
        print(f"Error en transmisión de video: {e}")

# Inicializar texto de bienvenida
mostrar_texto("Sistema iniciado")

# Iniciar hilos
audio_tx_thread = threading.Thread(target=enviar_audio, daemon=True)
command_thread = threading.Thread(target=procesar_comandos, daemon=True)
video_thread = threading.Thread(target=transmitir_video, daemon=True)

audio_tx_thread.start()
command_thread.start()
video_thread.start()

try:
    # Mantener el programa principal vivo
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nServicio detenido")
    # Añadir apagado del motor NUEVO
    pwm.ChangeDutyCycle(0)#HASTAAC
    device.clear()
    picam2.stop()
    pwm.stop()
    GPIO.cleanup()
    video_sock.close()
    command_sock.close()
    audio_tx_sock.close()
    text_sock.close()
    audio_rx_sock.close()