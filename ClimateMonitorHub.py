# Nome do projeto: ClimateMonitorHub
# Programador: Davidson Oliveira
import asyncio
import random

import uuid
from azure.iot.device.aio import IoTHubDeviceClient                                                                                     
from azure.iot.device import Message                                                                                                    

CONEXAO_DISPOSITIVO = "HostName=ClimateMonitorHub.azure-devices.net;DeviceId=Sensor_Climate_001;SharedAccessKey=YourAccessKeyHere"

INTERVALO_ENVIO = 2  # Enviar mensagens a cada 2 segundos
TEMPO_MAX_ENVIO = 30  # Limite de tempo de 30 segundos para envio de mensagens


TEMPERATURA_BASE = 22.0  # Temperatura (graus Celsius)
UMIDADE_BASE = 55.0  # Umidade (%)

LIMITE_ALERTA_TEMPERATURA = 28.0

TEMPLATE_MENSAGEM = '{"temperatura": %.2f, "umidade": %.2f, "alerta": "%s"}'

async def monitorar_ambiente():
    try:
       
        cliente = IoTHubDeviceClient.create_from_connection_string(CONEXAO_DISPOSITIVO)
        await cliente.connect()

        print("Monitorando ambiente e enviando dados para o ClimateMonitorHub...")

        while True:
            
            temperatura = TEMPERATURA_BASE + random.uniform(-5, 5)
            umidade = UMIDADE_BASE + random.uniform(-10, 10)
            alerta = "SIM" if temperatura > LIMITE_ALERTA_TEMPERATURA else "NÃO"
            
            conteudo_mensagem = TEMPLATE_MENSAGEM % (temperatura, umidade, alerta)
            mensagem = Message(conteudo_mensagem)
            
            mensagem.message_id = str(uuid.uuid4())
            mensagem.content_type = "application/json"
            mensagem.custom_properties["alerta"] = alerta

            print(f"Enviando: {conteudo_mensagem}")
            await cliente.send_message(mensagem)
            await asyncio.sleep(INTERVALO_ENVIO) 

    except Exception as e:
        print(f"Erro ao conectar ou enviar mensagem: {e}")
    finally:
        await cliente.shutdown()
        print("Conexão com o ClimateMonitorHub finalizada")

if __name__ == '__main__':
    try:
        asyncio.run(monitorar_ambiente())
    except KeyboardInterrupt:
        print("Monitoramento interrompido pelo usuário.")

