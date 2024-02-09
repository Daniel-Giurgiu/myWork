from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.resources import path
import json
import counters
from threading import Thread

class LengthError(Exception):
    """Raised when entered value is too long"""
    pass

class AgeError(Exception):
    """Raised when the age value is negative"""
    pass


class Member:
    def __init__(self, id, firstName, lastName, age):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
    
    @property   #getter
    def firstName(self):
        return self._firstName
    
    @property   #getter
    def lastName(self):
        return self._lastName
    
    @property   #getter
    def age(self):
        return self._age

    @firstName.setter
    def firstName(self, value):
        if len(value) > 10:
            raise LengthError
        self._firstName= value
        
    @lastName.setter
    def lastName(self, value):
        if len(value) > 10:
            raise LengthError
        self._lastName= value
        
    @age.setter
    def age(self, value):
        if value < 0:
            raise AgeError
        self._age= value

    def __repr__(self):
        return f"{self.id}; { self.firstName}; {self.lastName}; {self.age}"
lista = []
lista.append(Member(1, 'Alex', 'Ilie', 48 ))
lista.append(Member(2, 'Marin', 'Ion', 52 ))
lista.append(Member(3, 'George', 'Vasile', 26 ))
lista.append(Member(4, 'Maria', 'Gheorghe', 38 ))
print(lista)


class VerseBible:
    def __init__(self, id, verse):
        self.id = id
        self.verse = verse
    def __repr__(self):
        return f"{self.id}; {self.verse}"
lista_verse = []
lista_verse.append (VerseBible(1, 'Fiindcă atât de mult a iubit Dumnezeu lumea, încât L-a dat pe singurul Lui Fiu, pentru ca oricine crede în El să nu piară, ci să aibă viață veșnică.'))
lista_verse.append (VerseBible(2, 'Pot totul în Hristos, care mă întărește.'))
lista_verse.append (VerseBible(3, 'Frumos este să lăudăm pe Domnul și să mărim Numele Tău, Preaînalte, să vestim dimineața bunătatea Ta și noaptea credincioșia Ta'))
print(lista_verse)


class MyServer(BaseHTTPRequestHandler):
    def send_json(self, status, body_json):
        self.send_response(status)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(bytes(str(body_json), "utf8"))
    
    def send_text(self, status, body_text):
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(str(body_text), "utf8"))
    

    def do_GET(self):
        path = self.path
        path = path.split("/")
        if self.path == "/members" and self.command == "GET":
            counters.incrementEndpointCallCount(self.path, self.command)
            self.send_json(200, lista)
            
        elif path[1] == "members" and path[2].isdigit() and self.command == "GET":
            counters.incrementEndpointCallCount(self.path, self.command)
            get_id = int(path[2])
            for obj in lista:
                if obj.id == get_id:
                    self.send_json(200, obj)
            
        elif self.path == "/request_counts":
            counters.incrementEndpointCallCount(self.path, self.command)
            self.send_json(200, counters.counts)

        else:
            self.send_text(404, "Not found 404")
            
            
    def do_POST(self):
        if self.path == "/members" and self.command == "POST":
            counters.incrementEndpointCallCount(self.path, self.command)
            
            l = []
            for obj in lista:
                i = obj.id
                l.append(i)
            l.sort()
            new_id = l[-1] + 1

            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len).decode('utf8')
            body = json.loads(body)
            try:
                m = Member(
                new_id,
                body["firstName"],
                body["lastName"],
                int(body["age"])
                )
                lista.append(m)
                self.send_json(200, lista)
            except LengthError:
                self.send_text(400, "!!! 'firstName' and 'lastName' should be shorter than 10 characters !!!")
            except AgeError:
                self.send_text(400, "!!! 'age' should be positive value !!!")
            
        else:
            self.send_text(404, "Not found 404")

    
    def do_PATCH(self):
        path = self.path
        path = path.split("/")
        if path[1] == "members" and path[2].isdigit() and self.command == "PATCH":
            counters.incrementEndpointCallCount(self.path, self.command)
            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len).decode('utf8')
            body = json.loads(body)
            patch_id = int(path[2])
            try:
                for obj in lista:
                    if obj.id == patch_id:
                        if obj.firstName != body["firstName"]:
                            obj.firstName = body["firstName"]

                        if obj.lastName != body["lastName"]:
                            obj.lastNmae = body["lastName"]
                
                        if obj.age != int(body["age"]):
                            obj.age = int(body["age"])
                self.send_json(200, lista)
            except LengthError:
                self.send_text(400, "!!! 'firstName' and 'lastName' should be shorter than 10 characters !!!")
            except AgeError:
                self.send_text(400, "!!! 'age' should be positive value !!!")
            
        else:
            self.send_text(404, "Not found 404")


    def do_PUT(self):
        path = self.path
        path = path.split("/")
    
        if path[1] == "members" and path[2].isdigit() and self.command == "PUT":
            counters.incrementEndpointCallCount(self.path, self.command)
            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len).decode('utf8')
            body = json.loads(body)
            put_id = int(path[2])
            try:
                for obj in lista:
                    if obj.id == put_id:
                        obj.firstName = body["firstName"]
                        obj.lastName = body["lastName"]
                        obj.age = int(body["age"])
                self.send_json(200, lista)
            except LengthError:
                self.send_text(400, "!!! 'firstName' and 'lastName' should be shorter than 10 characters !!!")
            except AgeError:
                self.send_text(400, "!!! 'age' should be positive value !!!")
            
        else:
            self.send_text(404, "Not found 404")    
    
            
    def do_DELETE(self):
        global lista
        path = self.path
        path = path.split("/")
        if path[1] == "members" and path[2].isdigit() and self.command == "DELETE":
            counters.incrementEndpointCallCount(self.path, self.command)
            del_id = int(path[2])
            for obj in lista:
                if obj.id == del_id:
                    lista.remove(obj)
            
            self.send_json(200, lista)

        else:
            self.send_text(404, "Not found 404")

def response_member():
    #def main():
    PORT = 9000
    hostName = 'localhost'
    server = HTTPServer((hostName, PORT) , MyServer)
    print('Server running on port %s %s' % (PORT, hostName))
    server.serve_forever()

class MyBibleVerse(BaseHTTPRequestHandler):
    def send_json(self, status, body_json):
        self.send_response(status)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(bytes(str(body_json), "utf8"))
    
    def send_text(self, status, body_text):
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(str(body_text), "utf8"))

    def do_GET(self):
        path = self.path
        path = path.split("/")
        if path[1] == "verse" and path[2].isdigit() and self.command == "GET":
            get_id = int(path[2])
            for obj_verse in lista_verse:
                if obj_verse.id == get_id:
                    self.send_json(200, obj_verse)
   
    thread = Thread(target = response_member)
    thread.start()

def main():
    PORT = 8080
    hostName = 'localhost'
    server = HTTPServer((hostName, PORT) , MyBibleVerse)
    print('Server running on port %s %s' % (PORT, hostName))
    server.serve_forever()
main()

