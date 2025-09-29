import socket

def receive_output(conn):
    # First receive the length of the output
    output_length = int(conn.recv(4096).decode())
    output = ""
    received = 0
    while received < output_length:
        chunk = conn.recv(min(4096, output_length - received)).decode()
        output += chunk
        received += len(chunk)
    return output

def main():
    host = input("Enter the server IP address to connect to: ").strip()
    port = 45200

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(client.recv(4096).decode())  # Receive "connected" message

    while True:
        command = input("Enter command (or 'exit' to quit): ")
        client.send(command.encode())
        if command.lower() == "exit":
            break
        output = receive_output(client)
        print(output)
    client.close()

if __name__ == "__main__":
    main()
