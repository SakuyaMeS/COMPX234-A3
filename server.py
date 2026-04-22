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

def print_stats():
    while True:
        time.sleep(10)
        with lock:
            tuple_count = len(tuple_space)
            avg_key_size = 0
            avg_value_size = 0
            avg_tuple_size = 0

            if tuple_count > 0:
                total_key_size = sum(len(k) for k in tuple_space.keys())
                total_value_size = sum(len(v) for v in tuple_space.values())
                avg_key_size = total_key_size / tuple_count
                avg_value_size = total_value_size / tuple_count
                avg_tuple_size = avg_key_size + avg_value_size
        
            print("\n--- Tuple Space Stats ---")
            print(f"Tuples: {tuple_count}")
            print(f"Avg Tuple Size: {avg_tuple_size:.2f}")
            print(f"Avg Key Size: {avg_key_size:.2f}")
            print(f"Avg Value Size: {avg_value_size:.2f}")
            print(f"Clients: {total_clients}")
            print(f"Operations: {total_operations}")
            print(f"READs: {read_count}")
            print(f"GETs: {get_count}")
            print(f"PUTs: {put_count}")
            print(f"Errors: {error_count}\n")
