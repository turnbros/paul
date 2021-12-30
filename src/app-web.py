import os
import json
import workflows
import intent_routes
from waitress import serve
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

workflow_catalog = workflows.WorkflowCatalog()

@app.route("/")
def hello():
    return "Hello, my name is Paul!"


@app.route("/healthz")
def healthz():
    return "I feel healthy and alive!"


@app.route("/api/v1/workflows", methods=["GET"])
def get_workflows():
    Response(workflow_catalog.workflows.items(), status=200, content_type="application/json")


@app.route("/api/v1/workflows", methods=["PUT"])
def register_workflow():
    worker_registration = json.loads(request.data)
    worker_name = worker_registration["name"]
    print(worker_name)
    if workflow_catalog.register_workflow(worker_name):
        return "", 204
    return "", 500


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
    bind_ip = os.getenv("BIND_IP", "0.0.0.0")
    bind_port = int(os.getenv("BIND_PORT", 8443))
    serve(app, host=bind_ip, port=bind_port)

if __name__ == "__main__":
    start_webserver()