import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, my name is (development) Paul!"

@app.route("/healthz")
def healthz():
    return "I feel healthy and alive!"

@app.route("/api/v1/workflow", methods=["PUT"])
def register_workflow():
    pass

@app.route("/api/v1/fulfillment", methods=["POST"])
def fulfillment():
    json.loads(request.data)
    return "Hello, my name is (development) Paul!"

bind_ip = os.getenv("BIND_IP", "0.0.0.0")
bind_port = int(os.getenv("BIND_PORT", 8443))
debug_mode = bool(os.getenv("DEBUG_PAUL", False)) # Yes, any ENV var value will cause Paul to run in debug.

Flask.run(app, host=bind_ip, port=bind_port, debug=debug_mode)