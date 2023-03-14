import socket, random, time, threading, datetime

PORT = 1330
HOST = "172.31.112.1"
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
cod = 0
med_list = []

def rng():
    while True:
        measure = 0
        measure_time = str(datetime.datetime.now())
        if len(med_list):
            measure = med_list.pop(0)
        else:
            measure = max(random.random() * random.randint(1, 20), 0.1)
            measure = round(measure, 2)

        #print(f"===ENVIANDO MEDIDA: {measure} KW===")
        measure = str(measure)
        message = cod + ";" + measure_time + ";" + measure
        med_socket.sendto(message.encode(FORMAT), ADDR)
        time.sleep(10)

print("===MEDIDOR INICIADO===")

def get_num(initial_num, insert_msg, error_msg):
    num = initial_num
    while not num:
        try:
            num = input(insert_msg)
            if float(num):
                break
            else:
                print(error_msg)
        except Exception as e:
            print(error_msg)
            continue
    return num

med_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cod = get_num(cod, "INSIRA O CÓDIGO NÚMERICO DO MEDIDOR: ", "CÓDIGO INVÁLIDO.")
rng_thread = threading.Thread(target=rng)
rng_thread.start()

while True:
    print("===CONTROLE DO MEDIDOR===")
    manual_insert = get_num(0, "DIGITE UMA MEDIDA MANUAL PARA ENVIAR:", "MEDIDA INVÁLIDA.")
    if manual_insert:
        med_list.append(manual_insert)
