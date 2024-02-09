from custom_framework import CustomWebFramework, Identificator


app = CustomWebFramework(__name__)


@app.route("/simple/", method="GET")
def simple(self):
    print("simple handler")
   
   
@app.route("/get/<id>", method="GET")
def home(self):
    identificator = Identificator()
    id = identificator.get_value_of("id")
    
    print("Get handler! id = %s" % id )

   
@app.route("/get/<customer>/<order>/", method="get")
def add(self):
    identificator = Identificator()
    customer = identificator.get_value_of("customer")
    order = identificator.get_value_of("order")
    
    print(customer, order)

     
app.run()

