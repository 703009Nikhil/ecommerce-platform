from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return "✅ Product Service Running Successfully!"

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    output = []
    for p in products:
        output.append({"id": p.id, "name": p.name, "price": p.price, "stock": p.stock})
    return jsonify(output)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=6001)
