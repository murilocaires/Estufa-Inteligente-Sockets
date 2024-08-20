import socket
import threading
import time

sensor_id = "umidade"
leitura = 40
irrigacao_action = False
max_umidade = 80
step = 1

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


def aumentar_umidade_gradualmente():
    global leitura, irrigacao_action, max_umidade, step

    irrigacao_action = True  # Ativa o controle de ação para o aquecedor

    while leitura < max_umidade:
        if not irrigacao_action:
            print(f"Aumento de umidade interrompido: {leitura}°C")
            break
        leitura += step
        print(f"Aumentando umidade gradualmente: {leitura}°C")
        enviar_leitura()
        time.sleep(3)

    if leitura >= max_umidade:
        print("Umidade máxima atingida.")
        enviar_comando_atuador("irrigacao")  # Desligar o aquecedor
        irrigacao_action = False  # Desativa o controle de ação


def escutar_comandos():
    global irrigacao_action
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8082))
    server.listen(1)
    print("Sensor escutando na porta 8081.")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}.")
        command = client_socket.recv(1024).decode('utf-8')

        if "LIGAR" in command:
            irrigacao_action = True
            threading.Thread(target=aumentar_umidade_gradualmente).start()

        if "DESLIGAR" in command:
            irrigacao_action = False  # Parar o aumento de umidade
            print("Comando recebido para desligar.")

        client_socket.close()


if __name__ == '__main__':
    threading.Thread(target=escutar_comandos, daemon=True).start()

    while True:
        enviar_leitura()
        time.sleep(3)
