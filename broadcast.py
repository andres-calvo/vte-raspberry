import netifaces as ni
import socket
def get_broadcast_address():
    interfaces = ni.interfaces()
    for interface in interfaces:
        try:
            # Get interface addresses
            addrs = ni.ifaddresses(interface)
            # Check if there's an IPv4 address associated with the interface
            if ni.AF_INET in addrs:
                ip_info = addrs[ni.AF_INET][0]
                # Get broadcast address
                broadcast_address = ip_info.get('broadcast')
                if broadcast_address:
                    return broadcast_address
        except KeyError:
            # Ignore interfaces that don't have an IP address
            pass
    return None

# Obtener la IP local de la máquina
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectarse a un servidor remoto (no se envía ningún dato en realidad)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

