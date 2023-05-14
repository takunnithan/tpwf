import socket
import time
import concurrent.futures
import threading


def connection_handler(client_socket, client_address):
    print(f"=============== From Thread: {threading.get_ident()}")
    # print(f"Received connection from {client_address[0]}:{client_address[1]}")

    # Receive the request data from the client
    request_data = client_socket.recv(1024).decode('utf-8')
    # print(f"Received request:\n{request_data}")

    # Process the request (you can implement your own logic here)
    # For example, you can parse the request data to extract the HTTP method, headers, and body

    """"
    TODO: Write a HTTP parser for this - Preferably a Class with helper functions etc 

    GET / HTTP/1.1
    Host: localhost:8000
    Connection: keep-alive
    sec-ch-ua: "Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Sec-Fetch-Site: none
    Sec-Fetch-Mode: navigate
    Sec-Fetch-User: ?1
    Sec-Fetch-Dest: document
    Accept-Encoding: gzip, deflate, br
    Accept-Language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6
    """

    time.sleep(3)

    # Send a response back to the client
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world!"
    client_socket.sendall(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


def run():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the host and port to listen on
    host = '127.0.0.1'  # Replace with your desired host
    port = 8000  # Replace with your desired port
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    # Start listening for incoming connections
    server_socket.listen(10)
    print(f"Server listening on {host}:{port}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="tpwf") as executor:
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            """"
            
            TODO: create a handler function with threading ???? Async (Event loop) ??? multi-processing ??
            
            """
            future = executor.submit(connection_handler, client_socket, client_address)
            # print(future)


if __name__ == "__main__":
    run()


# TODO:
#   1. Handler with threads ( Thread pool / Queue requests if they exceed )
#   2. HTTP Parser -> The output of a Parser is a HTTP request object, HTTP Request
#   3. Routing
#       1. Registering methods with routes with decorator - keeping list / map of functions
#   4. HTTP Response class with helper function to create responses
#   5. More features
#       1. Middleware support ( Auth, session , etc - A Generic way ) - Registering like routes with Decorator
#           - Hooking functions along the way - they all return return a request / response object
#       2. Session , Cookie support
#       3. Templating - Jinja or something - Don't build it - use existing
#   6. Take inspiration from Flask & Django
#   7. WSGI implementation for support with NGINX / other servers
#   8. Use Typing
