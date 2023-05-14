import socket
import time
import threading
from http_parser import HttpParser


def connection_handler(client_socket, client_address):
    print(f"=============== From Thread: {threading.get_ident()}")
    # print(f"Received connection from {client_address[0]}:{client_address[1]}")

    # Receive the request data from the client
    connection_data = client_socket.recv(1024).decode('utf-8')
    # print(f"Received request:\n{connection_data}")

    http_request = HttpParser.parse(connection_data)
    print("============================")
    print(http_request)
    print("============================")

    # Send a response back to the client
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world!"
    client_socket.sendall(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


def run():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 9000

    server_socket.bind((host, port))

    server_socket.listen(10)
    print(f"Server listening on {host}:{port}")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5, thread_name_prefix="tpwf") as executor:
    while True:
        client_socket, client_address = server_socket.accept()

        # TODO: Async (Event loop) ?
        thread = threading.Thread(target=connection_handler, args=(client_socket, client_address), daemon=True)
        thread.start()


if __name__ == "__main__":
    run()


# TODO:
#   1. Handler with threads ( Thread pool / Queue requests if they exceed )
#   2. HTTP Parser -> The output of a Parser is a HTTP request object, HTTP Request
#   3. Routing
#       1. Registering methods with routes with decorator - keeping list / map of functions
#   4. HTTP Response class with helper function to create responses
#       1. __init__, to_bytes(), etc
#   5. More features
#       1. Middleware support ( Auth, session , etc - A Generic way ) - Registering like routes with Decorator
#           - Hooking functions along the way - they all return return a request / response object
#       2. Session , Cookie support
#       3. Templating - Jinja or something - Don't build it - use existing
#   6. Take inspiration from Flask & Django
#   7. WSGI implementation for support with NGINX / other servers
#   8. Use Typing
#   9. Support for config file
#       1. Host , Port ?
#   10. Design the Interfaces
