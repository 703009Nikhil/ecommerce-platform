from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Pending")

@app.route('/')
def home():
    return "✅ Order Service Running Successfully!"

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    output = []
    for o in orders:
        output.append({
            "id": o.id,
            "user_id": o.user_id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "status": o.status
        })
    return jsonify(output)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        user_id=data['user_id'],
        product_id=data['product_id'],
        quantity=data['quantity']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=6002)
