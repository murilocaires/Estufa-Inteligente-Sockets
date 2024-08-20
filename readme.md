# Estufa Inteligente Rede usando SOCKETS

## Descrição
A aplicação "Estufa Inteligente" é um sistema projetado para monitorar e controlar as condições de uma estufa, como temperatura, umidade, luminosidade e nível de CO2. O sistema é composto por sensores e atuadores que se comunicam com um gerenciador central, permitindo a configuração e o controle remoto das variáveis da estufa.

## Componentes

### Sensores
- **Temperatura interna**: Monitora a temperatura dentro da estufa.
- **Umidade do solo**: Mede o nível de umidade do solo.
- **Nível de CO2**: Verifica a concentração de dióxido de carbono na estufa.

### Atuadores
- **Aquecedor**: Aumenta a temperatura quando ativado.
- **Resfriador**: Diminui a temperatura quando ativado.
- **Sistema de irrigação**: Aumenta a umidade do solo quando ativado.
- **Injetor de CO2**: Aumenta a concentração de CO2 quando ativado.

### Gerenciador
O Gerenciador atua como o servidor da aplicação, gerenciando a comunicação com os sensores e atuadores.

### Cliente
O Cliente pode configurar os parâmetros da estufa e solicitar leituras dos sensores.

## Princípio de Operação
O Gerenciador mantém as leituras dos sensores dentro de valores máximos e mínimos configurados, acionando atuadores conforme necessário.

## Requisitos Funcionais

### 1. Sensoriamento
1.1. Todos os sensores possuem um identificador único.  
1.2. Os sensores devem se conectar ao Gerenciador e se identificar.  
1.3. Após confirmação, os sensores enviam suas leituras a cada 1 segundo.

### 2. Atuadores
2.1. Todos os atuadores possuem um identificador único.  
2.2. Os atuadores devem se conectar ao Gerenciador e se identificar.  
2.3. O Gerenciador pode ligar ou desligar os atuadores.

### 3. Gerenciador / Servidor
3.1. O Gerenciador aceita conexões de sensores e atuadores.  
3.2. O Gerenciador armazena o último valor recebido de cada sensor.  
3.3. O Gerenciador controla os atuadores com base nas leituras dos sensores.  
3.4. O Gerenciador fornece ao Cliente a última leitura de cada sensor quando solicitado.

### 4. Monitoramento / Cliente
- O Cliente pode requisitar a última leitura de qualquer sensor ao Gerenciador. Ele monitora os sensores e os atuadores ligados. 


## Cabeçalho da requisições (IPv4 TCP) HTTP

#### Sensores: enviar_sensores
        f"POST /sensor/reading HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
#### Cliente: ver_sensores / ver_atuadores
        "GET /sensors HTTP/1.1\r\n"      /        "GET /atuators HTTP/1.1\r\n"     
        "Host: localhost\r\n"                
        "User-Agent: CustomClient/1.0\r\n"  
        "Accept: */*\r\n"                    
        "Connection: keep-alive\r\n"         
        "Accept-Encoding: gzip, deflate\r\n" 
        "\r\n" 
#### Atuadores: resfriador / irrigacao / co2_injetor aquecedor
        f"POST /actuator/control HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
1. Execute na seguinte ordem:
   ```bash
   servidor.py -> cliente.py -> sendores -> atuadores
