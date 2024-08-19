import socket

atuador_id = "co2_injetor"

def controlar_co2_injetor(acao):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))
    request = f"POST /actuator/control HTTP/1.1\r\nHost: localhost\r\n\r\nid={atuador_id}&action={acao}"
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()

if __name__ == '__main__':
    controlar_co2_injetor(True)  # Ligar a co2_injetor

    while True:
        user_input = input("Digite '1' para desligar a Co2 injetor: ")
        if user_input == '1':
            controlar_co2_injetor(False)  # Desligar a co2_injetor
            print("Co2 injetor desligada.")
            break
