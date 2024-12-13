import requests
import random
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2

# Configurando GPIO Campainha
# Pull-up físico / Aciona em Low
GPIO.setmode(GPIO.BCM)
PinoCampainha = 23  # Pino GPIO 23
GPIO.setup(PinoCampainha, GPIO.IN)

picam2 = Picamera2() # Facilita configuração da câmera

# Inicializando a câmera
try:
    picam2.start()
    print("\n\n\n\n\n\nCâmera inicializada com sucesso!")
except Exception as erro:
    print(f"Erro ao inicializar a câmera: {erro}")
    picam2 = None


# Função para enviar notificação
def EnviaNotificacao():
    # Configurações de Acesso
    api_token = "a6kw6bt6r85voypc21uqb3i4sn55h2"    # Chave de API
    user_key = "uhy4d2zcz15abrewnn7uc7ive2tj39"     # Chave de Usuário

    # Configurações de Mensagem de Texto
    mensagens = ["Há alguém na sua porta!",
                 "A campainha tocou!",
                 "Sua visita chegou!"]
    mensagem = mensagens[random.randint(0, 2)]

    # Caminho da imagem capturada
    imagem_path = "/home/gaiola/Desktop/ImagemCampainha/FotoCampainha.jpg"

    # Envio da Notificação
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": api_token,
        "user": user_key,
        "message": mensagem,
    }
    try:
        with open(imagem_path, "rb") as image_file:
            files = {"attachment": image_file}
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                print("Notificação enviada com sucesso!")
            else:
                print(f"Erro ao enviar notificação: {response.status_code}, {response.text}")
    except FileNotFoundError:
        print("Erro: Imagem não encontrada para envio.")


# Função para capturar foto
def FotoCampainha():
    if picam2:
        try:
            picam2.capture_file('/home/gaiola/Desktop/ImagemCampainha/FotoCampainha.jpg')
            print('Foto capturada!')
        except Exception as e:
            print(f"Erro ao capturar a foto: {e}")


# Loop principal
try:
    while True:
        if not GPIO.input(PinoCampainha):
            print("Campainha Pressionada!")
            FotoCampainha()
            EnviaNotificacao()

            # Impede spam
            time.sleep(10)
finally:
    if picam2:
        picam2.stop()
        print("Câmera desligada.")
    GPIO.cleanup()
