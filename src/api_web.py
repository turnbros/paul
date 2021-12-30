import os
import json
import intent_routes
from flask import Flask, request, jsonify

app = Flask(__name__)

intent_map = {
    "projects/paul-fmma/agent/intents/a4f46c93-b72e-4b26-bced-e492e53d45d6" : "server_count"
}

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
async def fulfillment():
    try:
        request_json = json.loads(request.data)
        intent_name = request_json["queryResult"]["intent"]["name"]
        intent_parameters = request_json["queryResult"]["parameters"]
        response_text = await intent_routes.execute_intent_workflow(intent_map[intent_name], name="fuckface")
    except Exception as error:
        response_text = "on no, I shit the bed :-("

    return jsonify({
        "fulfillmentText": response_text,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response_text]
                }
            }
        ]
    })

def start_webserver():
    app.run(host="0.0.0.0", port=8443, debug=False, use_reloader=False)