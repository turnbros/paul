import os
import sys
import json
import logging
import workflows
import intent_routes
from waitress import serve
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
workflow_catalog = workflows.WorkflowCatalog()
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

@app.route("/")
def hello():
    return "Hello, my name is Paul!"


@app.route("/healthz")
def healthz():
    return "I feel healthy and alive!"


@app.route("/api/v1/workflows", methods=["GET"])
def get_workflows():
    return jsonify(list(workflow_catalog.workflows.items()))

@app.route("/api/v1/workflows", methods=["PUT"])
def register_workflow():
    worker_registration = json.loads(request.data)
    worker_name = worker_registration["name"]
    logging.debug(f"Register workflow worker {worker_name}")
    if workflow_catalog.register_workflow(worker_name):
        return "", 204
    return "", 500


@app.route("/api/v1/fulfillment", methods=["POST"])
async def fulfillment():
    try:
        request_json = json.loads(request.data)
        intent_name = request_json["queryResult"]["intent"]["name"]
        intent_parameters = request_json["queryResult"]["parameters"]
        logging.info(f"Execute worker: {intent_name}")
        response_text = await intent_routes.execute_intent_workflow(intent_name, name="fuckface")
    except Exception as error:
        logging.error(error)
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
    bind_ip = os.getenv("BIND_IP", "0.0.0.0")
    bind_port = int(os.getenv("BIND_PORT", 8443))
    serve(app, host=bind_ip, port=bind_port, )

if __name__ == "__main__":
    start_webserver()