from broadcast import get_broadcast_address,get_local_ip,send_my_ip_to_broadcast
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

connected_event = threading.Event()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/connected':
            connected_event.set()


def main():
    broadcast_address = get_broadcast_address()
    ip_address = get_local_ip()

    def infinite_loop_broadcast():
        interval = 5  # seconds
        while True:
            if connected_event.is_set():
                break
            send_my_ip_to_broadcast(ip_address,broadcast_address)
            time.sleep(interval)

    httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
    connected_thread = threading.Thread(target=infinite_loop_broadcast)
    connected_thread.start()



if __name__ == '__main__':
    main()