#  coding: utf-8 
import socketserver
import socket
import os
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        if self.data:
            payload = self.data.decode().split()
            method,path = payload[0],payload[1]

            if method == "GET":
                if self.test_path(path):
                    if os.path.exists("./www{}/index.html".format(path)) and path.endswith("html"):
                        content = open( "./www{}".format(path),'r').read()
                        status = "HTTP/1.1 200 OK\r\n"
                        status_code = status.encode()
                        content_len = "Content-Length: {}\r\n".format(str(len(content)))
                        content_len_code = content_len.encode()
                        content_type = "Content-Type: text/html;\r\n"
                        content_type_code = content_type.encode()
                        content_boby = content.encode()
                        close = "Connection : close \r\n\r\n"
                        header = status_code + content_len_code+ content_type_code + close + '\r\n'+ content_boby                           
                        self.request.sendall(header)
                    elif os.path.exists("./www{}".format(path)) and path.endswith("css"):
                        content = open( "./www{}".format(path),'r').read()
                        status = "HTTP/1.1 200 OK\r\n"
                        status_code = status
                        content_len = "Content-Length: {}\r\n".format(str(len(content)))
                        content_type = "Content-Type: text/css;\r\n"
                        content_type_code = content_type
                        content_len_code = content_len

                        content_boby = content
                        close = "Connection : close \r\n\r\n"
                        header = status_code + content_len_code + content_type_code + close + '\r\n'+ content_boby                          
                        self.request.sendall(header.encode())
                    elif os.path.exists("./www{}".format(path)) and path.endswith("html"):
                        content = open( "./www{}".format(path),'r').read()
                        status = "HTTP/1.1 200 OK\r\n"
                        status_code = status
                        content_len = "Content-Length: {}\r\n".format(str(len(content)))
                        content_type = "Content-Type: text/html;\r\n"
                        content_type_code = content_type
                        content_len_code = content_len

                        content_boby = content
                        close = "Connection : close \r\n\r\n"
                        header = status_code + content_len_code + content_type_code + close + '\r\n'+ content_boby                          
                        self.request.sendall(header.encode())
                    elif os.path.exists("./www{}/index.html".format(path)) and path.endswith("/"):
                        path = "./www{}index.html".format(path)
                        if open( path,'r').read():
                            content = open( path,'r').read()

                            status = "HTTP/1.1 200 OK\r\n"
                            status_code = status
                            content_len = ("Content-Length: {}\r\n".format(str(len(content))))
                            content_type = "Content-Type: text/html;\r\n"
                        
                            content_type_code = content_type
                            content_boby = content
                            close = "Connection : close \r\n\r\n"
                            content_len_code = content_len
                            header = status_code + content_len_code + content_type_code + close + '\r\n'+ content_boby                           
                            self.request.sendall(header.encode())
                        else:
                            self.request.send("HTTP/1.1 404 Not Found".encode())  
                    
                    else:
                        if os.path.isfile("./www{}/index.html".format(path)):
                            status_code = "HTTP/1.1 301 Moved Permanently"
                            location= "Location: http://127.0.0.1:8080{}/".format(path)
                            header = "{0}\r\n{1}\r\n{2}".format(status_code, location, "\r\n").encode()
                            self.request.sendall(header)
                        else:
                            self.request.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())  
                else : self.request.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())  
            else:self.request.send("HTTP/1.1 405 Method Not Allowed".encode())

    def test_path(self,path):
        return os.path.realpath(os.getcwd()+'/www' +path).startswith(os.getcwd()+'/www')


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
