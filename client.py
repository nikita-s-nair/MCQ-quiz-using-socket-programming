import socket
import sys
import time

def connect_to_server():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('LocalHost', 12345)

    try:
        # Connect to the server
        client_socket.connect(server_address)
        return client_socket

    except Exception as e:
        print(f"An error occurred while connecting to the server: {e}")
        return None

def communicate_with_server(client_socket):
    try:
        # Increase the timeout for receiving data
        client_socket.settimeout(60)  # 60 seconds timeout

        while True:
            data = client_socket.recv(1024).decode()
            if data:
                print(data)
                if "Your final score" in data:
                    break
                response = input("Your answer: ").strip().lower()
                client_socket.sendall(response.encode())

    except socket.timeout:
        print("Timeout occurred. Quiz ended.")
    except Exception as e:
        print(f"An error occurred during communication with the server: {e}")
    finally:
        client_socket.close

def main():
    while True:
        client_socket = connect_to_server()
        if client_socket is not None:
            communicate_with_server(client_socket)
            break
        else:
            print("Retrying connection in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()
