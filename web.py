import http.server
import socketserver
import setting_funtion as setting


def start_web():
    Handler = http.server.SimpleHTTPRequestHandler
    PORT = setting.web.port("port_web")
    #setting up website
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
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
def respone(item):
    pass






start_web()