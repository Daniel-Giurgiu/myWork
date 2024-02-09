import os
import threading
from flask import Flask, Response, json, request, session, render_template, send_from_directory, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import uuid
from PIL import Image
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-db", "--hostname", help="Database name")
parser.add_argument("-u", "--rezname", help="rez name")
parser.add_argument("-p", "--password", help="Password")

args = parser.parse_args()


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + args.rezname + ':' + args.password + "@localhost:3306/" + args.hostname

db = SQLAlchemy(app)
app.app_context().push()

class Persons(db.Model):
  __tablename__ = "Persons"
  ID = db.Column(db.Integer, primary_key = True)
  FirstName = db.Column(db.String(30))
  LastName = db.Column(db.String(30))
  height = db.Column(db.Integer) 
  thumbnail = db.Column(db.String(500))
  bigpath = db.Column(db.String(500))
    
  def __init__(self, ID, FirstName, LastName, height, thumbnail, bigpath):
      self.id = ID
      self.FirstName = FirstName
      self.LastName = LastName
      self.height = height
      self.thumbnail = thumbnail
      self.bigpath = bigpath

  def __repr__(self):
      return f"{self.id}; {self.FirstName}; {self.LastName}; {self.height}; {self.thumbnail}; {self.bigpath}"  

class Messages(db.Model):
  __tablename__ = "Messages"
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(45))
  message = db.Column(db.String(500))
  
  def __init__(self, id, email, message):
      self.id = id
      self.email = email
      self.message = message
      

  def __repr__(self):
      return f"{self.id}; {self.email}; {self.message}" 


queuue = []

@app.route("/js/<path:filename>")
def jss(filename):
  return send_from_directory("js", filename)
  
@app.route("/imag/<path:filename>")
def imagine(filename):
    return send_from_directory("/home/daniel/Desktop/photodesc/", filename)
   
@app.route("/css/<path:filename>")
def css(filename):
  return send_from_directory("css", filename)

@app.route("/", methods = ['GET'])
def nav():

  return render_template("base.html")

@app.route("/GET", methods = ['GET'])
def get():
  rezs = Persons.query.all()
  return render_template("get.html", usr = rezs)



@app.route("/add", methods = ['POST'])
def post():  
    file = request.files.get('photo', '')
    print(file)
    file_name = uuid.uuid4()
    filename, file_extension = os.path.splitext(file.filename)
    bigpath = str(file_name) + file_extension
    file.save("/home/daniel/Desktop/photodesc/"+bigpath)
    queuue.append(bigpath)
    
    
    img = Image.open("/home/daniel/Desktop/photodesc/"+bigpath)
    img.format.lower() in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'] 
    print(bigpath)

    rez = Persons(0,
        request.form.get("FirstName"),
        request.form.get("LastName"),
        request.form.get("height"),
        "small_" + bigpath,
        bigpath     
    )
    print(rez) 
    db.session.add(rez)
    db.session.commit()
        
    data = { "bigpath": bigpath,
        "status": "success"}
    return Response(json.dumps(data), mimetype='application/json'), 200

    
    
    
def thread_function():
    while True:
        if len(queuue) > 0:
            
            img = Image.open("/home/daniel/Desktop/photodesc/" + queuue[len(queuue)-1])
            img2 = img.resize((50, 60))
            thumbnail = "small_"+ queuue[len(queuue)-1]
            img2.save("/home/daniel/Desktop/photodesc/"+thumbnail)
            print(queuue[len(queuue)-1])
            queuue.pop()
           
x = threading.Thread(target=thread_function)
x.start()           

   
     
@app.route("/addm", methods = ['POST', 'GET'])
def postm():
    
    if request.method == 'POST':
        rez = Messages(
            request.form["id"],
            request.form["email"],
            request.form["message"],  
        )
        db.session.add(rez)
        db.session.commit()
        return render_template("message_return.html")
    else:
        return render_template("message.html")
    
    
      
@app.route("/update/<name>/<int:id>", methods = ['PUT'])
def put(id, name):
    rez = Persons.query.get_or_404(id)
    
    if name == "FirstName":
        rez.FirstName = request.form["FirstName"]
        db.session.commit()
    elif name == "LastName":
        rez.LastName = request.form["LastName"]
        db.session.commit()
    elif name == "height":
        rez.height = request.form["height"]
        db.session.commit()
        
    data = {"status": "success"}
    return data, 200


    
@app.route("/GET/<int:id>", methods = ['DELETE'])
def delete(id):
    rez = Persons.query.get_or_404(id)
    db.session.delete(rez)
    db.session.commit()
    return render_template("get.html")
    
    
if __name__ == "__main__":
  app.run()