import socket
import sys
import threading
import time

tuple_space = {}
total_clients = 0
total_operations = 0
read_count = 0
get_count = 0
put_count = 0
error_count = 0
lock = threading.Lock()

def receive_n(sock, num_bytes):
    data = b""
    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))
        if not chunk:
            break
        data += chunk
    return data