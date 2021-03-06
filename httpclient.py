#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Andrew Smith
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
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        lines = data.split('\r\n')
        line = lines[0].split(' ')
        code = 500
        if (len(line)>1):
            try:
                code = int(line[1])
            except:
                pass
        return code

    def get_headers(self,data):
        return None

    def get_body(self, data):
        lines = data.split('\r\n')
        write=False
        body=''
        for line in lines:
            if (line==''):
                write=True
                continue
            if (write):
                body += line
        
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500

        parse = urllib.parse.urlparse(url)
        
        path = parse.path
        host = parse.hostname
        port = 80
        try:
            if (parse.port != None):
                port = parse.port
        except:
            pass
        if (path==''):
            path='/'

        self.connect(host,port)
        
        requestLine = "GET " + path + " HTTP/1.1\r\n"
        headers = "Host: {}\r\n\r\n".format(host)

        request = requestLine + headers
        
        self.sendall(request)
        response = self.recvall(self.socket)

        self.close()

        body = self.get_body(response)
        code = self.get_code(response)

        print(body)
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        parse = urllib.parse.urlparse(url)
        
        path = parse.path
        host = parse.hostname
        port = 80
        try:
            if (parse.port != None):
                port = parse.port
        except:
            pass
        if (path==''):
            path='/'

        self.connect(host,port)

        length = 0
        payload = ''
        if (args != None):
            for key, value in args.items():
                payload += key+'='+value+'&'
            payload = payload[:-1]
            length = len(payload.encode('utf-8'))
            
        
        requestLine = "POST " + path + " HTTP/1.1\r\n"
        headers = "Host: {}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n".format(host,length)

        request = requestLine + headers + payload
        
        self.sendall(request)
        response = self.recvall(self.socket)

        self.close()

        body = self.get_body(response)
        code = self.get_code(response)

        print(body)
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
