#  coding: utf-8 
import SocketServer, os
#http://www.acmesystems.it/python_httpd
#http://stackoverflow.com/questions/22083359/send-text-http-over-python-socket
#http://stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only
#http://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python
#https://en.wikipedia.org/wiki/HTTP_301
# Copyright 2016 Kieran Boyle
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




class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.requestContent = self.data.split()
        if len(self.data) > 0:
            if self.requestContent[0]!= "GET":
                self.request.sendall("OK\n")
            else:
                #self.request.sendall("It's serving y'all\n")
                self.serve()

    def serve(self):
        self.mimetype = ''
        self.css_suffix = ".css"
        self.html_suffix = ".html"
        self.directory = "./www"
        #todone implement the mimetype functionality

        self.valid = False
	'''
        if self.requestContent[1] == "/":
            self.requestContent[1]= "/index.html"
            self.valid = True
        elif self.requestContent[1] == "/deep/":
            self.requestContent[1] = "/deep/index.html"
            self.valid = True

      
        elif self.requestContent[1] == "/deep":
            self.request.sendall('HTTP/1.1 301 Moved Permanently\r\n')
            self.request.sendall('Location: /deep/ \r\n\r\n')
	    self.requestContent[1] = "/deep/index.html"
            self.valid = True
        '''
	
	if self.requestContent[1].endswith("/"):
	    self.requestContent[1]= self.requestContent[1]+"index.html"
	    self.valid = True


            
        if self.requestContent[1].endswith(self.css_suffix):
	    self.mimetype = 'text/css'
            self.valid = True
        elif self.requestContent[1].endswith(self.html_suffix):
            #self.request.sendall("It Works HTML\n")
            self.mimetype = 'text/html'
            self.valid = True
	elif not(self.requestContent[1].endswith("/")):
	    print(self.requestContent[1])
	    self.request.sendall('HTTP/1.1 301 Moved Permanently\r\n')
	    self.request.sendall('Location: '+self.requestContent[1]+'/ \r\n\r\n')
	    self.requestContent[1] = self.requestContent[1]+"/index.html"
	    self.valid = True			

        #self.request.sendall(self.directory+self.requestContent[1])
	if self.valid == True and os.path.exists(self.directory+self.requestContent[1]):
            #self.request.sendall("validFile\n")
            self.dirFile = open(self.directory+self.requestContent[1])
            self.request.sendall('HTTP/1.1 200 OK\r\n')
            self.request.sendall('Content-Type: '+self.mimetype+'\r\n\r\n')
            #self.request.sendall(directory+self.requestContent[1])
            self.request.sendall(self.dirFile.read())
            self.dirFile.close()
        else:
            self.request.sendall('HTTP/1.1 404 Not Found\r\n')
            self.request.sendall('Content-Type: text/html\r\n\r\n')
            self.request.sendall('<html><body> <h1>ERROR 404 \n</h1> Path '+self.requestContent[1]+' Not Found</html></body>')

         

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
