from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask('__main__')
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
 
ma = Marshmallow(app)

class Product():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description,price,qty):
        self.name = name
        self.description = description
        self. price = price
        self.qty = qty 

class  ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','description', 'price','qty')


product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description' ]
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


#@app.route('/product', methods=['GET'])
#def get_products():
    #all_products = Product.query.all()
    #result = products_schema.dump(all_products)
    #return jsonify(result.data)
     


if __name__ == '__main__':
    app.run(debug=True)