import socket, threading, datetime, json, API

#larsid.net/29000 (fora da UEFS)
#172.16.103.15:9000 (dentro do LABOTEC)
#user tec502
#senha: eunaoseiasenha

CLIENT_PORT = 2126
MEASURE_PORT = 1330
HOST = socket.gethostbyname(socket.gethostname())
CLIENT_ADDR = (HOST, CLIENT_PORT)
MEASURE_ADDR = (HOST, MEASURE_PORT)
FORMAT = 'utf-8'

host_header = 'Host: ' + HOST+":"+str(CLIENT_PORT) + "\n"

client_sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sv.bind(CLIENT_ADDR)
print("===PORTA DO CLIENTE ABERTA===")

measure_sv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
measure_sv.bind(MEASURE_ADDR)
print("===PORTA DO MEDIDOR ABERTA===")

print("\n===SERVIDOR ONLINE...===\n")

def handle_client(client, addr):
    '''
    metódo que lida com um cliente

    1. recebe uma request
    2. extrai a rota e possiveis parametros do corpo
    3. processa a request através da API
    4. envia uma resposta

    :param client: socket do cliente
    :param addr: endereço do cliente
    '''

    connected = True
    session_vars = {}
    print(f"\n===CONEXÃO COM {addr} ESTABELECIDA.===\n")
    try:
        while connected:
            msg = client.recv(1024).decode(FORMAT)
            msg = str(msg)

            if msg:
                print(f"\n==={addr} ENVIOU A REQUEST:===\n{msg}")
                route, param = translate(msg)

                api_method = hasattr(API, route)
                if api_method:
                    api_method = getattr(API, route)
                    response = api_method(param, host_header, session_vars)
                else:
                    response = API.bad_request(host_header)

                print(f"\n===ENVIANDO RESPOSTA:=== \n{response}")
                client.send(response.encode(FORMAT))

    except Exception as e:
        print(f"\n===OCORREU UM ERRO NA COMUNICAÇÃO COM {addr}.===")
        print(e)

def translate(message):
    '''
    metódo que extrai rota e body de uma request HTTP
    1. verifica se a rota é POST/PUT ou GET
    2. parte a string da request, separando o nome da rota e body
    :param message: request HTTP
    :return: rota e body em forma de dicionário
    '''

    if message.startswith("P"): #POST OR PUT
        #print("decoding p")
        message = message.split("{")

        header = message[0]
        route = header.split("HTTP")[0]
        route = route.replace(" /", "_")
        route = route.replace(" ", "")

        param = message[1]
        param = "{" + param
        param = json.loads(param)

    elif message.startswith("G"): #GET
        message = message.split("HTTP")
        header = message[0]
        route = header.split("HTTP")[0]
        route = route.replace(" /", "_")
        route = route.replace(" ", "")
        param = {}

    return route, param

def tcp_start():
    '''
    metódo do socket TCP para comunicação com clientes e funcionários
    1. procura conexão com cliente
    2. se encontrar, inicia uma thread para lidar com o cliente
    '''
    client_sv.listen(5)
    print(f"===SERVIDOR DO CLIENTE RODANDO EM {HOST}===" )
    print("==PROCURANDO POR CLIENTES...===")

    while True:
        client_socket, addr = client_sv.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

def udp_start():
    '''
    metódo do socket UDP para recepção de medidas
    1. recebe informação do medidor
    2. utiliza a API para inserir a medida
    '''
    while True:
        measure_info, address = measure_sv.recvfrom(1024)
        measure_info = str(measure_info.decode(FORMAT))
        if measure_info:
            print(f"\n===UM MEDIDOR ENVIOU A MENSAGEM:===\n{measure_info}")
            API.inserir_medida(measure_info.split(";"))

tcp_thread = threading.Thread(target=tcp_start)
udp_thread = threading.Thread(target=udp_start)
tcp_thread.start()
udp_thread.start()
