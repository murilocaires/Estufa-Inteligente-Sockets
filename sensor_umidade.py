import socket
import time

sensor_id = "umidade"
leitura = 38.3

def enviar_leitura():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))

    # Preparar o corpo da requisição
    body = f"id={sensor_id}&leitura={leitura}"

    # Construir a requisição com os novos cabeçalhos
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

if __name__ == '__main__':
    while True:
        print("\n------\n")
        enviar_leitura()
        time.sleep(10)
