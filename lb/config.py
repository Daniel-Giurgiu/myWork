from enum import Enum
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import argparse


class ServerType(Enum):
    ONE_THREAD = HTTPServer
    MULTI_THREADED = ThreadingHTTPServer
    
    
class Config():
    def __init__(self, servertype=ServerType.ONE_THREAD, hostName="127.0.0.1", port=8080):
        args = self.parse_args()
        
        self.Port = port
        self.HostName = hostName
        self.ServerType = servertype
           
        if args["type"] != None:
            self.ServerType = eval("ServerType.%s" % args["type"])
            
        if args["host"] != None:
            self.HostName = args["host"]
            
        if args["port"] != None:
            self.Port = args["port"]
        
    def parse_args(self):
        parser = argparse.ArgumentParser(description="An http server that can run on one or more threads")
        parser.add_argument("-t", "--type",help="specify server type. TYPE should be ONE_THREAD or MULTI_THREADED")
        parser.add_argument("-p", "--port", help="specify port")
        parser.add_argument("-host", "--host",help="specify host")
        
        args = vars(parser.parse_args())
        
        if args["type"] == "ONE_THREAD" or args["type"] == "MULTI_THREADED":
            return args
        if args["type"] == None: 
            return args
    
    def __call__(self, cls):
        class Wrapper(cls):
            cls.conf = self
            
        return Wrapper
    

@Config(ServerType.ONE_THREAD, hostName="127.0.0.1", port=8085)
class Application():
    def __init__(self, handler):
        self.handler = handler
        
    def run(self):
        server = self.conf.ServerType.value((self.conf.HostName, self.conf.Port), self.handler)
            
        try:
            print("Server started http://%s:%s" % (self.conf.HostName, self.conf.Port))
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        
        print("Server stopped.")
