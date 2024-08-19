import socket

def enviar_requisicao(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()

def ver_sensores():
    print("\n------\n")
    request = "GET /sensors HTTP/1.1\r\nHost: localhost\r\n\r\n"
    enviar_requisicao(request)

def ver_atuadores():
    print("\n------\n")
    request = "GET /atuators HTTP/1.1\r\nHost: localhost\r\n\r\n"
    enviar_requisicao(request)

if __name__ == '__main__':
    while True:
        print("\n1. Ver sensores\n2. Ver atuadores\n3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            ver_sensores()
        elif opcao == "2":
            ver_atuadores()
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")

