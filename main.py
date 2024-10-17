from broadcast import get_broadcast_address,get_local_ip

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