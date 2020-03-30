import os

from flask import Flask,jsonify
from flask_restful import Api
from threading import Thread
from event_loop import event_loop
from resources.product import Product


app = Flask(__name__)

app.config['DEBUG'] = True

api = Api(app)

@app.route("/")
def keep_alive():
    return jsonify({"message": "OK"},200)

api.add_resource(Product, '/product/<string:instanceid>')

if __name__ == '__main__':
    Thread(target=event_loop.run_forever,daemon=True).start()
    app.run(host="localhost",port=5000)
