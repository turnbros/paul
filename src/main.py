import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, my name is Paul!"

bind_ip = os.getenv("BIND_IP", "0.0.0.0")
bind_port = int(os.getenv("BIND_PORT", 443))
debug_mode = bool(os.getenv("DEBUG_PAUL", False)) # Yes, any ENV var value will cause Paul to run in debug.

Flask.run(app, host=bind_ip, port=bind_port, debug=debug_mode)