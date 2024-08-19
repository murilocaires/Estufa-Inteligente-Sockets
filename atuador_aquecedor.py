import socket

atuador_id = "aquecedor"

def controlar_aquecedor(acao):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))
    request = f"POST /actuator/control HTTP/1.1\r\nHost: localhost\r\n\r\nid={atuador_id}&action={acao}"
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()

if __name__ == '__main__':
    controlar_aquecedor(True)  # Ligar o aquecedor

    while True:
        user_input = input("Digite '1' para desligar o aquecedor: ")
        if user_input == '1':
            controlar_aquecedor(False)  # Desligar o aquecedor
            print("Aquecedor desligado.")
            break
