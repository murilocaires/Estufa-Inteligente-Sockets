import socket
import time

sensor_id = "co2"
leitura = 23.6

def enviar_leitura():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))
    request = f"POST /sensor/reading HTTP/1.1\r\nHost: localhost\r\n\r\nid={sensor_id}&leitura={leitura}"
    print("Server request: " +request)
    client.send(request.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()

if __name__ == '__main__':
    while True:
        print("\n------\n")
        enviar_leitura()
        time.sleep(10)
