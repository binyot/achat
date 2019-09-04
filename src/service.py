import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import time
import json
import database

class Chat(BaseHTTPRequestHandler):
    def __init__(self, db, request, client_address, server):
        self.db = db
        self.response_post = {
            "/users/add":       self.db.add_user,
            "/chats/add":       self.db.add_chat,
            "/chats/get":       self.db.get_chats_with_user,
            "/messages/add":    self.db.add_message,
            "/messages/get":    self.db.get_messages_in_chat
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
            self.respond_error(400, "Bad request.")
            return

        handle = self.response_post.get(self.path, None)
        if handle is None:
            self.respond_error(405, "Method not allowed")
            return
        try:
            self._set_headers(201)
            self.write_json(handle(**content))
        except Exception as e:
            self.respond_error(409, str(e))
            return
        self.db.commit()

    def write_text(self, text):
        self.wfile.write(text.encode("utf-8"))

    def write_json(self, rjson):
        self.wfile.write(json.dumps(rjson).encode("utf-8"))

    def read_json(self, length):
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def respond_error(self, code, msg):
        self._set_headers(code)
        self.write_json({"error": {
                            "status": code,
                            "message": msg
                            }
                        })


from functools import partial

def run(server_class, handler_class, addr, port):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Started httpd listening on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    db = database.Database(database.connect("chat.db"), "init.sql")
    Handler_Class = partial(Chat, db)
    try:
        run(HTTPServer, Handler_Class, "0.0.0.0", 9000)
    except KeyboardInterrupt:
        print("\nInterrupted\n")
