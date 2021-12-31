import os
import sys
import json
import logging
import workflows
import traceback
from waitress import serve
from flask import Flask, request, jsonify

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
    workflow_names = []
    workflow_list = workflow_catalog.workflows
    for workflow in workflow_list:
        workflow_names.append(workflow)
    return jsonify(workflow_names)


@app.route("/api/v1/fulfillment", methods=["POST"])
async def fulfillment():
    try:
        request_json = json.loads(request.data)
        print(request_json)
        intent_name = request_json["queryResult"]["intent"]["displayName"]
        intent_parameters = request_json["queryResult"]["parameters"]
        logging.info(f"Execute worker: {intent_name}")
        response_text = await workflow_catalog.execute_workflow(intent_name, **intent_parameters)
    except Exception as error:
        traceback.print_exc()
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


def register_workflow(workflow_name):
    logging.debug(f"Register workflow {workflow_name}")
    if workflow_catalog.register_workflow(workflow_name):
        logging.info(f"Workflow {workflow_name} registered")
    else:
        logging.error(f"Failed to register {workflow_name}")


def start_webserver():
    # Register all the workflow stubs.
    workflows = [
        "server_count"
    ]
    for workflow in workflows:
        register_workflow(workflow)

    # Start the webserver.
    bind_ip = os.getenv("BIND_IP", "0.0.0.0")
    bind_port = int(os.getenv("BIND_PORT", 8443))
    serve(app, host=bind_ip, port=bind_port)

if __name__ == "__main__":
    start_webserver()