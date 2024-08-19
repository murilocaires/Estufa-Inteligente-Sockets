import socket

atuador_id = "resfriador"

def controlar_resfriador(acao):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))
    request = f"POST /actuator/control HTTP/1.1\r\nHost: localhost\r\n\r\nid={atuador_id}&action={acao}"
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()

if __name__ == '__main__':
    controlar_resfriador(True)  # Ligar o resfriador

    while True:
        user_input = input("Digite '1' para desligar o resfriador: ")
        if user_input == '1':
            controlar_resfriador(False)  # Desligar o resfriador
            print("resfriador desligado.")
            break
