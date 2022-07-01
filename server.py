import socket
import random
import logging
from http import HTTPStatus

logging.basicConfig(level=logging.DEBUG)

HOST = "127.0.0.1"
PORT = random.randint(10000, 20000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Binding server on {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:

        conn.send("Hello, I am server!".encode("utf-8"))

        while True:

            data = conn.recv(1024)
            print("Received", data, "from", addr)

            if not data or data == b"close":
                print("Got termination signal", data, "and closed connection")
                conn.close()

            data = data.decode("utf-8")

            method_from_request = data.split(" /")[0]
            headers_from_request = data.split("\r\n")[1:]
            sub_str_with_status = data.split("\r\n")[0]

            try:
                status_from_request = int(sub_str_with_status.split(" ")[1].split("status=")[1])
                status = HTTPStatus(status_from_request)
            except:
                status = HTTPStatus(200)

            print("method:" + method_from_request)
            print(*headers_from_request)
            print("status:" + str(status))
            result = {
                "method": method_from_request,
                "headers_from_request": [headers_from_request],
                "status": status
            }
            result = str(result)
            print("RESULT" + result)
            conn.send(result.encode("utf-8"))
            conn.close()


