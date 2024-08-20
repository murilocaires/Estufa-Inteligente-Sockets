import socket
import threading
import time

sensor_id = "temperatura"
leitura = 22
aquecedor_action = False  # Controle de ação para o aquecedor
resfriador_action = False  # Controle de ação para o resfriador


def enviar_leitura():
    global sensor_id, leitura
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))

    # Preparar o corpo da requisição
    body = f"id={sensor_id}&leitura={leitura}"

    request = (
        f"POST /sensor/reading HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
    )

    print("Server request: " + request)
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()


def enviar_comando_atuador(actuator_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))

    # Preparar o corpo da requisição para desligar o atuador
    body = f"id={actuator_id}&action=False"

    request = (
        f"POST /actuator/control HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
    )

    print(f"Enviando comando para desligar {actuator_id}.")
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()


def aumentar_temperatura_gradualmente():
    global leitura, aquecedor_action
    max_temperatura = 30
    step = 1
    aquecedor_action = True  # Ativa o controle de ação para o aquecedor

    while leitura < max_temperatura:
        if not aquecedor_action:
            print(f"Aumento de temperatura interrompido: {leitura}°C")
            break
        leitura += step
        print(f"Aumentando temperatura gradualmente: {leitura}°C")
        enviar_leitura()
        time.sleep(3)

    if leitura >= max_temperatura:
        print("Temperatura máxima atingida.")
        enviar_comando_atuador("aquecedor")  # Desligar o aquecedor
        aquecedor_action = False  # Desativa o controle de ação


def diminuir_temperatura_gradualmente():
    global leitura, resfriador_action
    min_temperatura = 15
    step = 1
    resfriador_action = True  # Ativa o controle de ação para o resfriador

    while leitura > min_temperatura:
        if not resfriador_action:
            print(f"Redução de temperatura interrompida: {leitura}°C")
            break
        leitura -= step
        print(f"Diminuindo temperatura gradualmente: {leitura}°C")
        enviar_leitura()
        time.sleep(3)

    if leitura <= min_temperatura:
        print("Temperatura mínima atingida.")
        enviar_comando_atuador("resfriador")  # Desligar o resfriador
        resfriador_action = False  # Desativa o controle de ação


def escutar_comandos():
    global aquecedor_action, resfriador_action
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8081))
    server.listen(1)
    print("Sensor escutando na porta 8081.")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}.")
        command = client_socket.recv(1024).decode('utf-8')

        if "LIGAR" in command:
            if "AQUECEDOR" in command and not aquecedor_action:
                aquecedor_action = True
                threading.Thread(target=aumentar_temperatura_gradualmente).start()
            elif "RESFRIADOR" in command and not resfriador_action:
                resfriador_action = True
                threading.Thread(target=diminuir_temperatura_gradualmente).start()

        if "DESLIGAR" in command:
            if "AQUECEDOR" in command:
                aquecedor_action = False  # Parar o aumento de temperatura
            elif "RESFRIADOR" in command:
                resfriador_action = False  # Parar a diminuição de temperatura
            print("Comando recebido para desligar.")

        client_socket.close()


if __name__ == '__main__':
    threading.Thread(target=escutar_comandos, daemon=True).start()

    while True:
        enviar_leitura()
        time.sleep(3)
