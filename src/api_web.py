import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, my name is (development) Paul!"


@app.route("/healthz")
def healthz():
    return "I feel healthy and alive!"


@app.route("/api/v1/workflow", methods=["PUT"])
def register_workflow():
    workflow_json = json.loads(request.data)
    workflow_queue = workflow_json["queue"]
    workflow_namespace = workflow_json["namespace"]


@app.route("/api/v1/fulfillment", methods=["POST"])
def fulfillment():
    request_json = json.loads(request.data)
    intent_name = request_json["intent"]["name"]
    intent_parameters = request_json["queryResult"]["parameters"]
    return jsonify({
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "Text response from webhook"
                    ]
                }
            }
        ]
    })

def start_webserver():
    app.run(host="0.0.0.0", port=8443, debug=False, use_reloader=False)