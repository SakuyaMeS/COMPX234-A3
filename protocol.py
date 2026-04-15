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