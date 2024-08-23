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


## Cabeçalho da requisições (IPv4 TCP) EIP

#### Sensores: enviar_sensores
        POST /sensor/reading EIP/1.0 
        Cliente-IP: 127.0.0.1 
        Cliente-Porta: 54163 
        Servidor: localhost 
        Servidor-Porta: 8080 
        Codificado: utf-8 
        Tamanho: 137 bytes 
        id=umidade&leitura=5
#### Cliente: ver_sensores / ver_atuadores
        GET /sensors EIP/1.1 GET /atuadores EIP/1.1
        Cliente-IP: 127.0.0.1
        Cliente-Porta: 51735
        Servidor: localhost
        Servidor-Porta: 8080
        Codificado: utf-8
        Tamanho: 130 byts
#### Atuadores: resfriador / irrigacao / co2_injetor / aquecedor
        POST /actuator/control EIP/1.0
        Cliente-IP: 127.0.0.1
        Cliente-Porta: 51850
        Servidor: localhost
        Servidor-Porta: 8080
        Codificado: utf-8
        Tamanho: 139 byts
        id=irrigacao&action=true
## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
1. Execute na seguinte ordem:
   ```bash
   servidor.py -> cliente.py -> sendores -> atuadores
