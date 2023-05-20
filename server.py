import socket
import threading

from http_parser import HttpParser
from http_response import HttpResponse
from tpwf import TPWF


def connection_handler(client_socket, client_address):
    print(f"=============== From Thread: {threading.get_ident()}")
    # print(f"Received connection from {client_address[0]}:{client_address[1]}")

    # Receive the request data from the client
    connection_data = client_socket.recv(5120).decode('utf-8')
    # connection_data = client_socket.recv(5120)
    # print("============================")
    # print(connection_data)
    # print("============================")

    http_request = HttpParser.parse(connection_data)

    response_from_user = TPWF.route_request(http_request)
    if isinstance(response_from_user, HttpResponse):
        http_response = response_from_user.to_bytes()
    else:
        http_response = HttpResponse(response_from_user).to_bytes()
    client_socket.sendall(http_response)

    # Close the client socket
    client_socket.close()


def run():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TODO: This should be customizable from a config file / from the TPWF class
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


app = TPWF()


@app.get("/")
def hello_world(request):
    request.print_request()
    return "Hello World!, I am at the top of the world"


@app.get("/hello")
def hello_world(request):
    request.print_request()
    return "This is World!!!"


@app.get("/world")
def hello_world(request):
    request.print_request()
    return "This is Hello!!!"


@app.get("/test")
def hello_world(request):
    request.print_request()
    return HttpResponse("This is a test message", 403)


@app.post("/test1")
def hello_world(request):
    request.print_request()
    return HttpResponse("This is a test1 message", 201, {"Content-Type": "text/plain", "Random-Header": "Random value"})


if __name__ == "__main__":
    run()

# TODO:
#   Create a list of features for V1 - Freeze it
#   Add new features later - Move on to other projects and come back to this whenever feel like it.


# TODO:
#   5. More features
#       1. Middleware support ( Auth, session , etc - A Generic way ) - Registering like routes with Decorator
#           - Hooking functions along the way - they all return a request / response object
#       2. Session , Cookie support
#       3. Templating - Jinja or something - Don't build it - use existing
#   7. WSGI implementation for support with NGINX / other servers
#   8. Use Typing
#   9. Support for config file
#       1. Host , Port ?
#   10. Design the Interfaces
#   11. Installable - setup.py ??
#   12. Read me with installation and usage instructions + V1, V2 plans
