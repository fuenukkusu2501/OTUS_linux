import socket
from urllib.parse import urlparse, parse_qs


def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    request_lines = request.split('\r\n')

    request_line = request_lines[0]
    method, url, _ = request_line.split(' ')
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    status_code = 200
    if 'status' in query_params:
        try:
            status_code = int(query_params['status'][0])
        except ValueError:
            status_code = 200

    response_status = f'{status_code} OK' if status_code == 200 else f'{status_code}'

    response_headers = [
        f"Request Method: {method}",
        f"Request Source: {client_socket.getpeername()}",
        f"Response Status: {response_status}",
        f"Host: localhost:8080",
        "User-Agent: python-requests/2.31.0",
        "Connection: close"
    ]

    custom_headers = dict(line.split(': ') for line in request_lines[1:] if ': ' in line)
    if 'Connection' in custom_headers:
        response_headers[5] = f"Connection: {custom_headers['Connection']}"
    for key, value in custom_headers.items():
        if key not in ["Host", "User-Agent", "Connection"]:
            response_headers.append(f"{key}: {value}")

    response_body = '\r\n'.join(response_headers)

    response = (
        f"HTTP/1.1 {response_status}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"Connection: close\r\n\r\n"
        f"{response_body}"
    )

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Server listening on port 8080...")

    while True:
        client_socket, _ = server_socket.accept()
        handle_request(client_socket)


if __name__ == "__main__":
    start_server()






