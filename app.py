from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
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


@app.route('/user', methods=['POST'])
def add_user():
  name = request.json['name']
  password = request.json['password']
  email = request.json['email']
  

  new_person = User(name, password, email)

  db.session.add(new_person)
  db.session.commit()


  return product_schema.jsonify(new_person)

 
     


if __name__ == '__main__':
    app.run(debug=True)