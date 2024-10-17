from broadcast import get_broadcast_address,get_local_ip,send_my_ip_to_broadcast
import threading


def main():
    broadcast_address = get_broadcast_address()
    ip_address = get_local_ip()
    if broadcast_address:
        print(f"Broadcast address: {broadcast_address}")
    else:
        print("Broadcast address not found.")

    if ip_address:
        print(f"Ip address: {ip_address}")
    else:
        print("Ip address not found.")
        
    def send_ip_in_interval():
        send_my_ip_to_broadcast(ip_address,broadcast_address)
        threading.Timer(5, send_ip_in_interval).start()
    


if __name__ == '__main__':
    main()