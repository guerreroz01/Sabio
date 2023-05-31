from TTS.api import TTS

def speaker(summary):
    model_name = TTS.list_models()[25]
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
    tts.tts_to_file(text=summary, file_path="./output.wav", speed=1)
