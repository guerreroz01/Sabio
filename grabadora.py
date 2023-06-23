def grabar_audio():
    import pyaudio
    import wave

# Configuración de la grabación
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    DURACION_SEGUNDOS = 5
    ARCHIVO_SALIDA = "grabacion.wav"

# Inicializar PyAudio
    audio = pyaudio.PyAudio()

# Abrir el stream de audio
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Grabando audio...")

# Lista para almacenar los fragmentos de audio
    frames = []

# Grabar audio en fragmentos
    for i in range(0, int(RATE / CHUNK * DURACION_SEGUNDOS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("¡Grabación finalizada!")

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


