import os
from flask import Flask, jsonify, abort, send_file, request, Response, json, send_from_directory
import argparse
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

parser = argparse.ArgumentParser()
parser.add_argument("-db", "--hostname", help="Database name")
parser.add_argument("-u", "--rezname", help="rez name")
parser.add_argument("-p", "--password", help="Password")
args = parser.parse_args()

migrate = Migrate()
ma = Marshmallow()
cors = CORS()

def create_app():
    app = Flask(__name__)
    migrate.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    return app

app = create_app()

#  1.    GET METHOD
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    ionut = req_path.split(".")
    if len(ionut) > 1  and req_path != '':
      WORDS = ""
      with open("/home/daniel/Desktop/driveEx/"+req_path, "r") as file:
        for line in file.readlines():
          WORDS = WORDS + line.rstrip()
      return WORDS
    else:
      BASE_DIR = '/home/daniel/Desktop/driveEx'

      # Joining the base and the requested path
      abs_path = os.path.join(BASE_DIR, req_path)

      # Return 404 if path doesn't exist
      if not os.path.exists(abs_path):
          return abort(404)

      # Check if path is a file and serve
      if os.path.isfile(abs_path):
          return send_file(abs_path)

      # Show directory contents
      files = os.listdir(abs_path)
      print(files)
      return  jsonify(files)

# POST METHOD FOR FOLDERS

@app.route('/add', methods = ['POST'])
def adauga():
  filename = request.form.get("name")
  os.makedirs('/home/daniel/Desktop/driveEx/' + filename)
  data = {"status": "success"}
  return Response(json.dumps(data), mimetype='application/json'), 200

# POST METHOD FOR FILES

@app.route('/addf', methods = ['POST'])
def adaugaF():
  filename = request.form.get("name")
  os.makedirs('/home/daniel/Desktop/driveEx/' + filename)
  data = {"status": "success"}
  return Response(json.dumps(data), mimetype='application/json'), 200


if __name__ == "__main__":
  app.run()

