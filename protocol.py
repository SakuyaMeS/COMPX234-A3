def encode_request(command, key, value=None):
    if command == "READ":
        body = f" R {key}"
    elif command == "GET":
        body = f" G {key}"
    elif command == "PUT":
        body = f" P {key} {value}"
    else: raise ValueError("Invalid command!")

    message = f"{len(body) + 3:03d}{body}"
    return message

def decode_request(message):
    body = message[3:]

    if body.startswith(" R "):
        key = body[3:]
        return "READ", key, None
    elif body.startswith(" G "):
        key = body[3:]
        return "GET", key, None
    elif body.startswith(" P "):
        content = body[3:]
        parts = content.split(" ", 1)
        if len(parts) != 2:
            raise ValueError("Invalid PUT request")
        key = parts[0]
        value = parts[1]
        return "PUT", key, value
    else:
        raise ValueError("Invalid request format")
    
def encode_response(success, command, key, value=None):
    if success:
        if command == "READ":
            body = f" OK ({key}, {value}) read"
        elif command == "GET":
            body = f" OK ({key}, {value}) removed"
        elif command == "PUT":
            body = f" OK ({key}, {value}) added"
        else:
            raise ValueError("Invalid command")
    else:
        if command == "PUT":
            body = f" ERR {key} already exists"
        elif command == "READ" or command == "GET":
            body = f" ERR {key} does not exist"
        else:
            raise ValueError("Invalid command")
        
    message = f"{len(body) + 3:03d}{body}"
    return message

def recv_exact(sock, n):
    data = b""

    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return None
        data += chunk

    return data.decode()