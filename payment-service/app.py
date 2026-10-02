from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")

@app.route('/')
def home():
    return "✅ Payment Service Running Successfully!"

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    output = []
    for p in payments:
        output.append({
            "id": p.id,
            "order_id": p.order_id,
            "amount": p.amount,
            "status": p.status
        })
    return jsonify(output)

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.json
    new_payment = Payment(
        order_id=data['order_id'],
        amount=data['amount'],
        status="Completed"
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Payment processed successfully!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=6003)
