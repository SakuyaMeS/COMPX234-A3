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

def increment_stat(stat_name):
    global total_clients, total_operations, read_count, get_count, put_count, error_count

    if stat_name == "total_clients":
        total_clients += 1
    elif stat_name == "total_operations":
        total_operations += 1
    elif stat_name == "read_count":
        read_count += 1
    elif stat_name == "get_count":
        get_count += 1
    elif stat_name == "put_count":
        put_count += 1
    elif stat_name == "error_count":
        error_count += 1