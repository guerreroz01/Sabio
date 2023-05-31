import subprocess
import time
import simpleaudio as sa
import openai
import io
from contextlib import redirect_stdout, redirect_stderr
from TTS.api import TTS

fake_stdout = io.StringIO()

with open('api_token.txt', 'r') as f:
    api_key = f.read().rstrip('\n')

openai.api_key = api_key 

def listar_modelos():
    listas = openai.Model.list().data
    for l in listas:
        print(l.id)


def logg(summary):
    with open('output.txt', 'a') as f:
        f.write(summary + '\n')


def speaker(summary):
    model_name = TTS.list_models()[25]
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
    tts.tts_to_file(text=summary, file_path="./output.wav", speed=1)


def chat():
    messages_template = []
    messages_template.append(
        {
            "role": "system",
            "content": f"Manten una conversación amena y responde todas las preguntas sin recomendaciones todas las palabras deben estar sin tilde"
        }
    )

    try:
        while True:
            input_user=input("\nUsuario: ")

            print("\n")
            if input_user == "/salir":
                break

            elif input_user == "/role":
                new_role = input("define un nuevo role: ")
                messages_template[0]["content"] = f"a partir de ahora actuaras como si fueras un: '{new_role}' seras un asistente preciso, conciso y que te atengas al rol que se te ha dado, no deberas bajo ningun caso hacer recomendaciones, todas las palabras de tus respuestas no deben contener tilde"
            
            elif input_user == "/role?":
                print(messages_template[0])

            else:
                messages_template.append({
                    "role": "user",
                    "content": f"{input_user}"
                })

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages_template,
                    stream=True
                )

                collected_chunks = []
                collected_messages = []
                
                print("Sabio:\n")
                for chunk in response:
                    print(chunk['choices'][0]['delta'].get('content', ''), end='')
                    collected_chunks.append(chunk)
                    chunk_message = chunk['choices'][0]['delta']
                    collected_messages.append(chunk_message)

                print("\n")
                summary = ''
                for m in collected_messages:
                    summary += m.get('content', '')


                messages_template.append({
                    "role": "assistant",
                    "content": f"{summary}"
                })

                if len(messages_template) == 10:
                    messages_template.pop(1)

                    
                with redirect_stdout(fake_stdout):
                    speaker(summary)


                logg(f"<< {input_user}")
                logg(f">> {summary}")

                wave_obj = sa.WaveObject.from_wave_file("./output.wav")
                play_obj = wave_obj.play()
                play_obj.wait_done()
                subprocess.run(["killall", "vlc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    except openai.error.ServiceUnavailableError as e:
        print(f"OpenAI API returned an API Error: {e}")
        pass

    except openai.error.RateLimitError as e:
        print(f"Al parecer sabio está ocupado, esperando 5s para volver ha hacer la pregunta")
        pass

chat()
