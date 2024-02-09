import os
from flask import Flask, Response, json, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import uuid
from PIL import Image
import argparse
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

parser = argparse.ArgumentParser()
parser.add_argument("-db", "--hostname", help="Database name")
parser.add_argument("-u", "--rezname", help="rez name")
parser.add_argument("-p", "--password", help="Password")
args = parser.parse_args()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + args.rezname + ':' + args.password + "@localhost:3306/" + args.hostname
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    return app

class Persons(db.Model):
  __tablename__ = "Persons"
  ID = db.Column(db.Integer, primary_key = True)
  FirstName = db.Column(db.String(30))
  LastName = db.Column(db.String(30))
  height = db.Column(db.Integer) 
  thumbnail = db.Column(db.String(500))
  bigpath = db.Column(db.String(500))
    
  def __init__(self, ID, FirstName, LastName, height, thumbnail, bigpath):
      self.ID = ID
      self.FirstName = FirstName
      self.LastName = LastName
      self.height = height
      self.thumbnail = thumbnail
      self.bigpath = bigpath

  def __repr__(self):
      return f"{self.ID}; {self.FirstName}; {self.LastName}; {self.height}; {self.thumbnail}; {self.bigpath}"  

class PersonsShema(ma.Schema):
    class Meta:
        fields = ("ID","FirstName", "LastName", "height", "thumbnail", "bigpath")
persons_schema = PersonsShema()
persons_schema = PersonsShema(many=True)
queuue = []
app = create_app()

@app.route("/js/<path:filename>")
def jss(filename):
  return send_from_directory("js", filename)
  
@app.route("/imag/<path:filename>")
def imagine(filename):
    return send_from_directory("/home/daniel/Desktop/photodesc/", filename)

#  1.    GET METHOD

@app.route("/GET", methods = ['GET'])
def get():
  rezs = Persons.query.all()
  results = persons_schema.dump(rezs)
  return jsonify(results)

#  2.    POST 

@app.route("/add", methods = ['POST'])
def post(): 
    file = request.files.get('photo')
    file_name = uuid.uuid4()
    filename, file_extension = os.path.splitext(file.filename)
    bigpath = str(file_name) + file_extension
    file.save("/home/daniel/Desktop/photodesc/"+bigpath)
    queuue.append(bigpath)
    
    img = Image.open("/home/daniel/Desktop/photodesc/"+bigpath)
    img.format.lower() in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'] 
    if len(queuue) > 0:
        img = Image.open("/home/daniel/Desktop/photodesc/" + queuue[len(queuue)-1])
        img2 = img.resize((50, 60))
        thumbnail = "small_"+ queuue[len(queuue)-1]
        img2.save("/home/daniel/Desktop/photodesc/"+thumbnail)
        print(queuue[len(queuue)-1])
        queuue.pop()

    rez = Persons(0,
        request.form.get("FirstName"),
        request.form.get("LastName"),
        request.form.get("height"),
        "small_" + bigpath,
        bigpath     
    )
    db.session.add(rez)
    db.session.commit()
    data = { "bigpath": bigpath,
        "status": "success"}
    return Response(json.dumps(data), mimetype='application/json'), 200
    
    
    
#  3.    PUT METHOD FOR PHOTOS
@app.route("/update/<int:id>/photo", methods = ['PUT'])
def putP(id):
    if request.files.get('photo'):
        file = request.files.get('photo')
        file_name = uuid.uuid4()
        filename, file_extension = os.path.splitext(file.filename)
        bigpath = str(file_name) + file_extension
        file.save("/home/daniel/Desktop/photodesc/"+bigpath)
        queuue.append(bigpath)
        
        img = Image.open("/home/daniel/Desktop/photodesc/"+bigpath)
        img.format.lower() in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'] 
        if len(queuue) > 0:
            img = Image.open("/home/daniel/Desktop/photodesc/" + queuue[len(queuue)-1])
            img2 = img.resize((50, 60))
            thumbnail = "small_"+ queuue[len(queuue)-1]
            img2.save("/home/daniel/Desktop/photodesc/"+thumbnail)
            print(queuue[len(queuue)-1])
            queuue.pop()
            rez = Persons.query.get_or_404(id)
            rez.bigpath = bigpath
            rez.thumbnail = thumbnail
            db.session.commit()
        data = {"status": "success"}
        return data, 200

# PUT METHOD FOR FORM

@app.route("/update/<int:id>", methods = ['PUT'])
def put(id):  
    rez = Persons.query.get_or_404(id)
    rez.FirstName = request.form["FirstName"]
    rez.LastName = request.form["LastName"]
    rez.height = request.form["height"]
    
    db.session.commit()
    data = {"status": "success"}
    return data, 200

#  4.    DELETE METHOD
 
@app.route("/GET/<int:id>", methods = ['DELETE'])
def delete(id):
    rez = Persons.query.get_or_404(id)
    db.session.delete(rez)
    db.session.commit()
    data = {"status": "success"}
    return data, 200
    
if __name__ == "__main__":
  app.run()