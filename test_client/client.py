import socket
import http.client
def main():
    buffer_size = 1024
    broadcast_port= 12345
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Hacer que el socket pueda reutilizar la dirección y puerto inmediatamente
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincular el socket al puerto local
    sock.bind(('', broadcast_port))  # El '' significa que escucha en todas las interfaces

    print(f"Escuchando paquetes broadcast en el puerto {broadcast_port}...")

    raspberry_ip = ""

    while raspberry_ip == "":
        # Esperar a recibir un paquete
        data, addr = sock.recvfrom(buffer_size)
        received_data = data.decode('utf-8')
        if "RASPBERRY" in received_data:
            raspberry_ip = received_data.split("-")[1]
        # Mostrar los datos recibidos y la dirección del remitente
        print(f"Paquete recibido desde {addr}: {data.decode('utf-8')}")

    conn = http.client.HTTPConnection(raspberry_ip,8000)
    conn.request("GET","/connected")
    #TODO MANEJAR SI NO LLEGA UN 200
    conn.close()

if __name__ == '__main__':
    main()