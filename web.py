import http.server
import socketserver
import setting_funtion as setting
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def respone(item):
    pass
def start_web():    
    PORT = setting.web.port("port_web")
    IP = setting.web.ip()
    Handler = http.server.SimpleHTTPRequestHandler
    #setting up website
    with socketserver.TCPServer((IP, int(PORT)), Handler) as httpd:
        try:
            httpd.serve_forever()
            print(PORT)
        except KeyboardInterrupt:
            print("\nStopping server.")
            httpd.server_close()

    #setting up listen
    pass
    #start chat loop
    pass




