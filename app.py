import os
from flask import Flask
from flask import jsonify
from flask import request
import json
from cerberus import Validator
from exceptions import payLoadIsMissing
from exceptions import malformedJson
from exceptions import payloadNotMatchingSchema
from exceptions import NoAPIKeyPresent
import payments
from logger import Logger
LOG = Logger()

app = Flask(__name__)


@app.errorhandler(NoAPIKeyPresent)
@app.errorhandler(payLoadIsMissing)
@app.errorhandler(payloadNotMatchingSchema)
@app.errorhandler(malformedJson)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


payload_input_schema = {
                    'payload': {'type': 'dict', 'required': True}
                    }



@app.route("/ping")
def ping():
    return "Pong!"

@app.route("/schema")
def schema():
    return json.dumps(dict(input=payload_input_schema))

@app.route("/", methods=['GET'])
def index():
    return 'Block-payments-comming'

@app.route("/", methods=['POST'])
def fn():
    v = Validator()
    v.schema = payload_input_schema
    payload = request.form.get('payload', None)
    if not(payload):
        raise payLoadIsMissing('There is no payload', status_code=500)
    try:
        payload = json.loads(payload)
    except:
        raise malformedJson("Payload present but malformed: {}".format(payload))
    #if v(payload):
    result = dict(success=True, payload=payments.result(payload))
    result = json.dumps(result)
    
    return result
    #else:
        #raise payloadNotMatchingSchema("Payload didn't match schema ({}\n{})".format(payload_input_schema, v.errors))
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)