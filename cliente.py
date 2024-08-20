import socket

# Função para enviar a requisição HTTP
def enviar_requisicao(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket usando IPv4 e TCP
    client.connect(("localhost", 8080))                         # Conecta ao servidor localhost na porta 8080
    client.send(request.encode('utf-8'))                        # Envia a requisição HTTP codificada em UTF-8
    response = client.recv(4096).decode('utf-8')                # Recebe a resposta e a decodifica em UTF-8
    print(response)                                             # Exibe a resposta recebida
    client.close()                                              # Fecha a conexão com o servidor

# Função para visualizar os sensores
def ver_sensores():
    print("\n------\n")
    request = (
        "GET /sensors HTTP/1.1\r\n"          # Linha de requisição: método GET para o recurso /sensors, usando HTTP/1.1
        "Host: localhost\r\n"                # Especifica o servidor de destino (localhost)
        "User-Agent: CustomClient/1.0\r\n"   # Indica o cliente que está fazendo a requisição
        "Accept: */*\r\n"                    # Informa que o cliente aceita qualquer tipo de conteúdo na resposta
        "Connection: keep-alive\r\n"         # Solicita que a conexão seja mantida aberta
        "Accept-Encoding: gzip, deflate\r\n" # Aceita resposta comprimida
        "\r\n"                               # Linha em branco para separar os cabeçalhos do corpo (não há corpo aqui)
    )
    enviar_requisicao(request)

# Função para visualizar os atuadores
def ver_atuadores():
    print("\n------\n")
    request = (
        "GET /atuators HTTP/1.1\r\n"         # Linha de requisição: método GET para o recurso /atuators, usando HTTP/1.1
        "Host: localhost\r\n"                # Especifica o servidor de destino (localhost)
        "User-Agent: CustomClient/1.0\r\n"   # Indica o cliente que está fazendo a requisição
        "Accept: */*\r\n"                    # Informa que o cliente aceita qualquer tipo de conteúdo na resposta
        "Connection: keep-alive\r\n"         # Solicita que a conexão seja mantida aberta
        "Accept-Encoding: gzip, deflate\r\n" # Aceita resposta comprimida
        "\r\n"                               # Linha em branco para separar os cabeçalhos do corpo (não há corpo aqui)
    )
    enviar_requisicao(request)

# Função para controlar os atuadores
def controlar_atuador(atuador_id, acao):
    # Valida o atuador e a ação
    valid_atuadores = ["aquecedor", "resfriador", "irrigacao", "co2_injetor"]
    if atuador_id not in valid_atuadores:
        print(f"Atuador '{atuador_id}' inválido!")
        return

    if acao not in [True, False]:
        print("Ação inválida!")
        return

    print("\n------\n")
    body = f"id={atuador_id}&action={str(acao).lower()}"  # Converte ação para string minúscula
    request = (
        f"POST /actuator/control HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
    )
    enviar_requisicao(request)

# Função principal com menu interativo
if __name__ == '__main__':
    while True:
        print("\n1. Ver sensores\n2. Ver atuadores\n3. Controlar atuador\n4. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            ver_sensores()
        elif opcao == "2":
            ver_atuadores()
        elif opcao == "3":
            atuador = input("Digite o atuador (aquecedor, resfriador, irrigacao, co2_injetor): ")
            acao_input = input("Digite 'on' para ligar ou 'off' para desligar: ").lower()
            acao = acao_input == 'on'
            controlar_atuador(atuador, acao)
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")
