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

def handle_client(client_socket):
    global tuple_space
    
    increment_stat("total_clients")
    try:
        while True:
            size_buffer = receive_n(client_socket, 3)
            if len(client_socket) < 3:
                break
            message_size = int(size_buffer.decode())
            message_buffer = receive_n(client_socket, message_size - 3)
            if len(message_buffer) < message_size - 3:
                break
            
            message = message_buffer.decode()
            response = handle_request(message)

            response_message = f"{len(response) + 4:03d} {response}"
            client_socket.sendall(response_message.encode())
    except (socket.error, ValueError):
        pass
    finally:
        client_socket.close()

def handle_request(message):
    global tuple_space
    increment_stat("total_operations")

    if len(message) < 3:
        increment_stat("error_count")
        return "ERR Invalid message"
    
    parts = message.split(" ", 2)
    if len(parts) < 2:
        increment_stat("error_count")
        return "ERR Invalid message"
    
    op = parts[0]
    key = parts[1]

    if len(key) > 999:
        increment_stat("error_count")
        return "ERR Key too long"
    
    with lock:
        if op == "R":
            increment_stat("read_count")
            if key in tuple_space:
                value = tuple_space[key]
                return f"OK ({key}, {value}) read"
            else:
                increment_stat("error_count")
                return f"ERR {key} does not exist"
        
        elif op == "G":
            increment_stat("get_count")
            if key in tuple_space:
                value = tuple_space.pop[key]
                return f"OK ({key}, {value}) removed"
            else:
                increment_stat("error_count")
                return f"ERR {key} does not exist"

        elif op == "P":
            increment_stat("put_count")
            
            if len(parts) < 3:
                increment_stat("error_count")
                return f"ERR Invalid PUT"
            
            value = parts[2]

            if len(value) > 999:
                increment_stat("error_count")
                return f"ERR Value too long"
            
            if len(key + " " + value) > 970:
                increment_stat("error_count")
                return f"ERR Tuple too long"
            
            if key in tuple_space:
                increment_stat("error_count") 
                return f"ERR {key} already exists"
            
            tuple_space[key] = value
            return f"OK ({key}, {value}) added"
    
    increment_stat("error_count")
    return "ERR Unknown operation"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)
    print(f"Server started on port {port}")

    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()