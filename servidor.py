import socket
import threading

# Armazenar leituras dos sensores e estado dos atuadores
leituras = {"temperatura": 0, "umidade": 0, "co2": 0}
atuadores = {"aquecedor": False, "resfriador": False, "irrigacao": False, "co2_injetor": False}

# Dicionário para mapear sensores a portas
sensor_ports = {
    "aquecedor": 8081,
    "resfriador": 8081,
    "irrigacao": 8082,
    "co2_injetor": 8083
}

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Recebido: {request}")

    # Processar a requisição HTTP
    if request.startswith("POST /sensor/reading"):
        process_sensor_reading(request)
        response = "HTTP/1.1 200 OK\r\n\r\nLeitura recebida."
    elif request.startswith("POST /actuator/control"):
        process_actuator_control(request)
        response = "HTTP/1.1 200 OK\r\n\r\nAtuador controlado."
    elif request.startswith("GET /sensors"):
        response = f"HTTP/1.1 200 OK\r\n\r\n{leituras}"
    elif request.startswith("GET /atuators"):
        response = f"HTTP/1.1 200 OK\r\n\r\n{atuadores}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\nPágina não encontrada."

    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def process_sensor_reading(request):
    global leituras

    # Extrair dados da requisição
    lines = request.splitlines()
    sensor_data = lines[-1].split('&')
    sensor_id = sensor_data[0].split('=')[1]
    leitura = float(sensor_data[1].split('=')[1])

    # Armazenar leitura atualizada
    leituras[sensor_id] = leitura
    print(f"Sensor {sensor_id} atualizado para {leitura}.")

def process_actuator_control(request):
    global atuadores
    # Extrair dados da requisição
    lines = request.splitlines()
    actuator_data = lines[-1].split('&')
    actuator_id = actuator_data[0].split('=')[1]
    action = actuator_data[1].split('=')[1].lower() == "true"

    atuadores[actuator_id] = action
    print(f"Atuador {actuator_id} {'ligado' if action else 'desligado'}.")

    # Enviar comando ao sensor
    if actuator_id in atuadores:
        command = f"{actuator_id.upper()}_{'LIGAR' if action else 'DESLIGAR'}"
        avisar_sensor(command, sensor_ports[actuator_id])  # Usar a porta correspondente

def avisar_sensor(message, porta):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", porta))

    client.send(message.encode('utf-8'))
    client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))  # Porta do servidor
    server.listen(5)
    print("Servidor iniciado na porta 8080.")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
