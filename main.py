from broadcast import get_broadcast_address,get_local_ip,send_my_ip_to_broadcast
import time


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

    # Run the function every 5 seconds
    interval = 5  # seconds

    while True:
        send_my_ip_to_broadcast(ip_address,broadcast_address)
        time.sleep(interval)

    


if __name__ == '__main__':
    main()