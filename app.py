from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(200))
  email = db.Column(db.String(200))
  

  def __init__(self, name, password, email):
    self.name = name
    self.password = password
    self.email = email
    


class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'password', 'email')


product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a new user
@app.route('/product', methods=['POST'])
def add_product():
  name = request.json['name']
  password = request.json['password']
  email = request.json['email']
  

  new_person = Product(name, password, email)

  db.session.add(new_person)
  db.session.commit()


  return product_schema.jsonify(new_person)

 
     


if __name__ == '__main__':
    app.run(debug=True)