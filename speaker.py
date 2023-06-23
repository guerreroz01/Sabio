import pyaudio
import wave
import threading

# Configuración de la grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
ARCHIVO_SALIDA = "grabacion.wav"

# Variable para controlar la grabación
grabacion_activa = threading.Event()

def grabar_audio():
    # Inicializar PyAudio
    audio = pyaudio.PyAudio()

    # Abrir el stream de audio
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Lista para almacenar los fragmentos de audio
    frames = []

    # Iniciar la grabación
    print("Grabación iniciada. Presiona Enter para detener la grabación.")

    # Función en segundo plano para detener la grabación al presionar Enter
    def detener_grabacion():
        input()
        grabacion_activa.clear()

    # Iniciar el hilo en segundo plano para detener la grabación
    thread = threading.Thread(target=detener_grabacion)
    thread.start()

    # Grabar audio en fragmentos hasta que se detenga la grabación
    grabacion_activa.set()
    while grabacion_activa.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    print("Grabación finalizada.")

    # Detener y cerrar el stream de audio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Guardar la grabación en un archivo WAV
    with wave.open(ARCHIVO_SALIDA, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Grabación guardada como '{ARCHIVO_SALIDA}'")
    return ARCHIVO_SALIDA


