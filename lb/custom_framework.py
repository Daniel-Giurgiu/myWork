from http import client
from http.server import BaseHTTPRequestHandler
from config import Application 


class Identificator:
    """
    Class properties:
        self.identificators = [{identificator: value}, {identificator, value}]
        
    Methods for the caller:
        - get_value_of(specified_identificator) --> str
    """
    
    def get_value_of(self, specified_identificator):
        """ Method return a string if specified_identificator exist """
        
        for identificator_obj in self.identificators:
            if specified_identificator in identificator_obj:
                identificator_value = identificator_obj[specified_identificator]
                
        return identificator_value
                       

class Handler(BaseHTTPRequestHandler):
    def execute_handlers(self, method):
        for func in self.handlers["decorated_functions"]:
            server_path = func["route"].split("/")
            client_path = self.path.split("/")
            
            if client_path[-1] == "":
                client_path.pop()
            if server_path[-1] == "":
                server_path.pop()

            if client_path[0] == "":
                client_path.pop(0)
            if server_path[0] == "":
                server_path.pop(0)

            # simple path
            if self.check_simple_path(server_path, client_path):
                if func["method"].lower() == method:
                    func["function"](self)
                
            # path with identificators
            identificators = self.extract_identificators(server_path, client_path)
            if identificators != None:
                if func["method"].lower() == method:
                    Identificator.identificators = identificators 
                    func["function"](self)

    
    def check_simple_path(self, server_path, client_path):
        if server_path == client_path:
            return True
        else:
            return False
        
    def extract_identificators(self, server_path, client_path):
        if len(server_path) == len(client_path):
            identif = []
            for i in range(len(server_path)):
                if server_path[i] != client_path[i]:
                    if server_path[i].split("<")[1].split(">")[0]:
                        idendificator = server_path[i].split("<")[1].split(">")[0]
                        value = client_path[i]
                        identif.append({idendificator:value})
                else:
                    continue
            return identif
        return None        
        
    def do_GET(self):
        self.execute_handlers("get")
           
    def do_POST(self):
        self.execute_handlers("post")
        
    def do_PUT(self):
        self.execute_handlers("put")
                    
    def do_DELETE(self):
        self.execute_handlers("delete")
                    
    def do_PATCH(self):
        self.execute_handlers("patch")


class CustomWebFramework:
    def __init__(self, name):
        self.handlers = {"decorated_functions":[]}
        self.name = name
                                                         
    def route(self, route, method="GET"):
        def Wrapper(func): 
            self.handlers["decorated_functions"].append({"function": func, "method": method, "route": route})
        return Wrapper

    def run(self):
        handler = Handler
        handler.handlers = self.handlers
        Application(handler).run()

