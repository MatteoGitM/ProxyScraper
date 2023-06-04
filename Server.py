import threading
import re
import cgi

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
  
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/api/v1/set/', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                data = cgi.parse_qs(self.rfile.read(
                    length), keep_blank_values=1)
                urlpath = self.path.split('/')[-1]
                print(data, ' ', urlpath)
            else:
                data = {}
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_GET(self):
        if None != re.search('/api/v1/getproxies/*', self.path):      
            global p_inventory    
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            proxy_list = p_inventory.export_list()
            self.wfile.write(proxy_list.encode('utf-8'))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port, inventory):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)     
        global p_inventory 
        p_inventory = inventory
        #self.server_ssl = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
        #self.server_ssl.socket = ssl.wrap_socket(self.server_ssl.socket, certfile='./cert.pem', server_side=True)
    
    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()
