import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import time
import json


class Chat(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.response_post = {
            "/users/add": self.handle_users_add,
            "/chats/add": self.handle_chats_add,
            "/chats/get": self.handle_chats_get,
            "/messages/add": self.handle_messages_add,
            "/messages/get": self.handle_messages_get
        }
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)


    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        try:
            content = self.read_json(length)
        except json.JSONDecodeError as e:
            self.respond_error(400)
            return

        handle = self.response_post.get(self.path, None)
        if handle is None:
            self.respond_error(405)
            return
        handle(content)

        self._set_headers()
        self.write_json({"echo": content})

    def write_text(self, text):
        self.wfile.write(text.encode("utf-8"))

    def write_json(self, rjson):
        self.wfile.write(json.dumps(rjson).encode("utf-8"))

    def read_json(self, length):
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def respond_error(self, code):
        self._set_headers(code)
        self.write_json({"error": code})

    def handle_users_add(self, args):
        pass

    def handle_chats_add(self, args):
        pass

    def handle_chats_get(self, args):
        pass

    def handle_messages_add(self, args):
        pass

    def handle_messages_get(self, args):
        pass

def run(server_class=HTTPServer, handler_class=Chat, addr="localhost", port=80):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Started httpd listening on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run(addr="localhost", port=9000)
    except KeyboardInterrupt:
        print("\nInterrupted\n")
