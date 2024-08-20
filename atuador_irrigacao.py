import socket

atuador_id = "irrigacao"

def controlar_irrigacao(acao):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))

    # Dados a serem enviados
    body = f"id={atuador_id}&action={str(acao).lower()}"  # Converte ação para string minúscula

    # Construindo o cabeçalho da requisição
    request = (
        f"POST /actuator/control HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
    )

    # Enviando a requisição
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()


if __name__ == '__main__':
    controlar_irrigacao(True)  # Ligar o irrigacao

    while True:
        user_input = input("Digite '1' para desligar a irrigacao: ")
        if user_input == '1':
            controlar_irrigacao(False)  # Desligar a irrigacao
            print("irrigacao desligada.")
            break
