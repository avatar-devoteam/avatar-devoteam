#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
	
    if req.get("result").get("action") != "rdvaction":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    ppl = parameters.get("name-visitor")

    rdv = {'Julien':'Manon', 'Jean':'Cyril', 'Victor':'Matthieu'}
	
    speech = "Le rdv de " + ppl + " est a " + str(rdv[ppl]) + " est-ce que c'est avec toi ?"

    print("Response:")
    
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        "contextOut": [{"name":"rdv-confirm", "lifespan":1, "parameters":{"name-visitor":ppl}}],
	"followupEvent":{"name":"rdvevent","data":{'Response':str(rdv[ppl])}},
        "source": "apiai-rdv-list"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
