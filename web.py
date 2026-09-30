
import socketserver
import setting_funtion as setting
import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class CustomHandler(BaseHTTPRequestHandler):
    """
    Custom handler to handle GET and POST requests, 
    parsing data sent by the front-end.
    """
    
    def do_GET(self):
        """Handle GET requests and extract query parameters."""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        print(f"Received GET path: {parsed_url.path}")
        print(f"Received GET query parameters: {query_params}")
        
        # Send response back to client
        response_data = {
            "status": "success",
            "method": "GET",
            "path": parsed_url.path,
            "received_params": query_params
        }
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

    def do_POST(self):
        """Handle POST requests and read body payload."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.wfile.read(content_length)
        
        parsed_url = urlparse(self.path)
        
        try:
            # Try parsing body as JSON if applicable
            if self.headers.get('Content-Type') == 'application/json':
                data = json.loads(post_body.decode('utf-8'))
            else:
                data = post_body.decode('utf-8')
        except Exception as e:
            data = str(post_body)

        print(f"Received POST path: {parsed_url.path}")
        print(f"Received POST data: {data}")

        # Send response back to client
        response_data = {
            "status": "success",
            "method": "POST",
            "path": parsed_url.path,
            "received_data": data
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode("utf-8"))




def start_web():    
    PORT = setting.web.port("port_listen")
    IP = setting.web.ip()
    
    # Use our custom handler instead of SimpleHTTPRequestHandler
    Handler = CustomHandler
    
    # Setting up website server
    with socketserver.TCPServer((IP, int(PORT)), Handler) as httpd:
        try:
            print(f"Serving at http://{IP}:{PORT}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")
            httpd.server_close()

start_web()