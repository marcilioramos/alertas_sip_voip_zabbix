#!/bin/python3
############################
# Autor: Marcilio Ramos
# Data: 06.02.2024
# Finalidade: Enviar alertas Zabbix usando VOIP - SIP
#
#############################
from gtts import gTTS
from pydub import AudioSegment
import subprocess
import time
import sys

texto = sys.argv[3]
with open('/tmp/output.txt', 'a') as file:
#    file.write(sys.argv[1])
    file.write(f'{texto}\n')

tts = gTTS(text=texto, lang='pt-br')

# Salvar o arquivo MP3 com as características padrão
tts.save("./output.mp3")

# Converter o arquivo MP3 para WAV com taxa de amostragem específica
audio = AudioSegment.from_mp3("./output.mp3")
audio = audio.set_frame_rate(8000)
audio.export("./output.wav", format="wav")

# Configurações SIP
usuario = "#####"
senha = "#####"
dominio_sip = "#####"
destino = sys.argv[1]
arquivo_wav = './output.wav'

# Iniciar a chamada usando linphonec
subprocess.run(["linphonecsh", "init"])
subprocess.run(["linphonecsh", "register", "--host", dominio_sip, "--username", usuario, "--password", senha])
subprocess.run(["linphonecsh", "generic", "soundcard use files"])

# Fazer a chamada
subprocess.run(["linphonecsh", "dial", destino])

# Reproduzir o arquivo .wav ao atender a chamada
subprocess.run(["linphonecsh", "generic", f"play {arquivo_wav}"])

# Aguardar a chamada ser atendida
tempo_ligacao = int(sys.argv[2])
time.sleep(tempo_ligacao)

# Encerrar a chamada
subprocess.run(["linphonecsh", "hangup"])

#Apagar os arquivos de audio
subprocess.run(["rm", "./output.mp3"])
subprocess.run(["rm", "./output.wav"])
