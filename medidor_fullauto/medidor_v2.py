import socket, random, time, threading, datetime

PORT = 1330
HOST = "172.16.103.3" #"172.16.103.212"
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
cod = str(random.randint(1, 6))
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


        measure = str(measure)
        message = cod + ";" + measure_time + ";" + measure
        print(f"===ENVIANDO MEDIDA: {message}===")
        med_socket.sendto(message.encode(FORMAT), ADDR)
        time.sleep(10)

print("===MEDIDOR INICIADO===")


med_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rng_thread = threading.Thread(target=rng)
rng_thread.start()
