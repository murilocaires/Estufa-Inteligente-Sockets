import socket

atuador_id = "resfriador"

def controlar_resfriador(acao):
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
    controlar_resfriador(True)  # Ligar o resfriador

    while True:
        user_input = input("Digite '1' para desligar o resfriador: ")
        if user_input == '1':
            controlar_resfriador(False)  # Desligar a resfriador
            print("resfriador desligada.")
            break
