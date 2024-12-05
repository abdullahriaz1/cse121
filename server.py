from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import requests

def get_public_ip():
    try:
        # Use an external service to get the public IP
        response = requests.get("https://api.ipify.org?format=text")
        if response.status_code == 200:
            return response.text
        else:
            return "Could not fetch public IP"
    except Exception as e:
        return f"Error fetching public IP: {e}"

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
    public_ip = get_public_ip()
    server = HTTPServer((host_name, 8000), MyHandler)
    print(f"Server running locally at http://{host_name}:8000/")
    print(f"Public IP address: {public_ip}")
    server.serve_forever()
