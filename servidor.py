import socket
import threading

# Armazenar leituras dos sensores e estado dos atuadores
leituras = {"temperatura": 0, "umidade": 0, "co2": 0}
atuadores = {"aquecedor": False, "resfriador": False, "irrigacao": False, "co2_injetor": False}

aquecedor = False

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Recebido: {request}")

    # Processar a requisição HTTP
    if request.startswith("POST /sensor/reading"):
        process_sensor_reading(request)
        response = "HTTP/1.1 200 OK\r -Leitura recebida."
    elif request.startswith("POST /actuator/control"):
        process_actuator_control(request)
        response = "HTTP/1.1 200 OK\r -Atuador controlado."
    elif request.startswith("GET /sensors"):
        response = f"HTTP/1.1 200 OK\r -{leituras}"
    elif request.startswith("GET /atuators"):
        response = f"HTTP/1.1 200 OK\r -{atuadores}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\nPágina não encontrada."

    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def process_sensor_reading(request):
    global leituras, atuadores

    # Extrair dados da requisição
    lines = request.splitlines()
    sensor_data = lines[-1].split('&')
    sensor_id = sensor_data[0].split('=')[1]
    leitura = float(sensor_data[1].split('=')[1])
    leituras[sensor_id] = leitura

    # aquecedor
    if atuadores["aquecedor"] and sensor_id == "temperatura":
        leitura += 5
    # resfriador
    if atuadores["resfriador"] and sensor_id == "temperatura":
        leitura -= 5

    # irrigacao
    if sensor_id == "umidade" and atuadores["irrigacao"]:
        leitura += 20

    # co2_injetor
    if sensor_id == "co2" and atuadores["co2_injetor"]:
        leitura += 3.5

    leituras[sensor_id] = leitura
    print(f"Sensor {sensor_id} atualizado para {leitura}.")


def process_actuator_control(request):
    global atuadores, leituras
    # Extrair dados da requisição
    lines = request.splitlines()
    actuator_data = lines[-1].split('&')
    actuator_id = actuator_data[0].split('=')[1]
    action = actuator_data[1].split('=')[1] == "True"

    atuadores[actuator_id] = action
    print(actuator_id)
    print(f"Atuador {actuator_id} {'ligado' if action else 'desligado'}.")



def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    print("Servidor iniciado na porta 8080.")

    while True:
        #A cada conexao com Cliente cria uma Thread
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    start_server()
