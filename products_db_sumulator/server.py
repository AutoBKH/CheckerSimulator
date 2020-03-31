import os
from flask import Flask, request, jsonify
server = Flask(__name__)
from test import product_test

def is_alive():
    return jsonify('product db simulator is up and running')

def return_message():
    if request.method == 'POST':
        product_test.delay_response = request.values['response']


def start():
    return jsonify(f"Starting simulator")


def stop():
    return jsonify(f"Stopping simulator")


def restart():
    return jsonify("Restarted simulator")


def shutdown():
    """
    Shuts down the server, only active when running the server locally
    """
    shutdown_function = request.environ.get("werkzeug.server.shutdown")
    if shutdown_function is None:
        raise ValueError("Cannot shutdown! Server is not running with werkzeug")
    shutdown_function()
    return "Server shutting down"


server.add_url_rule('/', view_func=return_message, methods=['POST'])
server.add_url_rule('/is_alive', view_func=is_alive)
server.add_url_rule('/start', view_func=start, methods=['POST'])
server.add_url_rule('/stop', view_func=stop, methods=['POST'])
server.add_url_rule('/restart', view_func=restart, methods=['POST'])
server.add_url_rule("/shutdown", "shutdown", view_func=shutdown, methods=["POST"])

if __name__ == "__main__":
    server.run(debug=True, host='0.0.0.0', port=5050)


