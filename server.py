from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests

# Fetch latitude and longitude using IP-API
def get_server_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            lat = data.get("lat", 0.0)
            lon = data.get("lon", 0.0)
            # Format to two decimal places
            return round(lat, 2), round(lon, 2)
        return 0.0, 0.0
    except Exception as e:
        print(f"Error fetching location: {e}")
        return 0.0, 0.0

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Fetch location information
        lat, lon = get_server_location()
        # Create a JSON response
        response = {"latitude": lat, "longitude": lon}
        # Send response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        # Get the content length of the incoming request
        content_length = int(self.headers['Content-Length'])
        # Read the body of the request
        post_data = self.rfile.read(content_length)

        # Log the received data
        print("Received POST data:", post_data.decode())

        # Process the data (assuming JSON for this example)
        try:
            data = json.loads(post_data)
            print("Parsed JSON:", json.dumps(data, indent=4))  # Pretty print received JSON
            response = {"status": "success", "received": data}
        except json.JSONDecodeError:
            print("Error: Invalid JSON")
            response = {"status": "error", "message": "Invalid JSON"}

        # Send a response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    server_address = ('', 8000)  # Serve on all interfaces at port 8000
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
