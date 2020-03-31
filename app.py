import os

from flask import Flask,jsonify,request
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

def shutdown():
    """
    Shuts down the server, only active when running the server locally
    """
    shutdown_function = request.environ.get("werkzeug.server.shutdown")
    if shutdown_function is None:
        raise ValueError("Cannot shutdown! Server is not running with werkzeug")
    shutdown_function()
    return "Server shutting down"

api.add_resource(Product, '/product/<string:instanceid>')
app.add_url_rule("/shutdown", "shutdown", view_func=shutdown, methods=["POST"])

if __name__ == '__main__':
    Thread(target=event_loop.run_forever,daemon=True).start()
    app.run(host="localhost",port=5000)
