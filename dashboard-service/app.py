from flask import Flask, render_template
import requests

app = Flask(__name__)

USER_SERVICE = "http://user:5000"
PRODUCT_SERVICE = "http://product:6001"
ORDER_SERVICE = "http://order:6002"
PAYMENT_SERVICE = "http://payment:6003"
NOTIFICATION_SERVICE = "http://notification:6004"

@app.route('/')
def dashboard():
    try:
        users = requests.get(f"{USER_SERVICE}/").text
        products = requests.get(f"{PRODUCT_SERVICE}/products").json()
        orders = requests.get(f"{ORDER_SERVICE}/orders").json()
        payments = requests.get(f"{PAYMENT_SERVICE}/payments").json()
        notifications = requests.get(f"{NOTIFICATION_SERVICE}/notifications").json()
    except Exception as e:
        return f"Error fetching data: {e}"

    return render_template("dashboard.html",
                           users=users,
                           products=products,
                           orders=orders,
                           payments=payments,
                           notifications=notifications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6005)
