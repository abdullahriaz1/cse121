from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, GET request received!")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"Received POST data: {post_data.decode()}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, POST request received!")

if __name__ == "__main__":
    host_name = socket.gethostbyname(socket.gethostname())
    server = HTTPServer((host_name, 8000), MyHandler)
    print(f"Server running at http://{host_name}:8000/")
    server.serve_forever()
