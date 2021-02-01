import socket

q = set()

def parse_links(response):
    return []


def fetch(url: str):
    sock = socket.socket()
    sock.connect(('xkcd.com', 80))
    request = f'GET {url} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    print(response.decode())
    # Page is now downloaded.
    links = parse_links(response)
    q.update(links)


fetch('/')