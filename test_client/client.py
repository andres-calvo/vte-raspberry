from broadcast import broadcast_port
import socket

def main():
    buffer_size = 1024
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Hacer que el socket pueda reutilizar la dirección y puerto inmediatamente
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincular el socket al puerto local
    sock.bind(('', broadcast_port))  # El '' significa que escucha en todas las interfaces

    print(f"Escuchando paquetes broadcast en el puerto {broadcast_port}...")

    while True:
        # Esperar a recibir un paquete
        data, addr = sock.recvfrom(buffer_size)
    
        # Mostrar los datos recibidos y la dirección del remitente
        print(f"Paquete recibido desde {addr}: {data.decode('utf-8')}")

if __name__ == '__main__':
    main()