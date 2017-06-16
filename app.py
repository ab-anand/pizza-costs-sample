import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def index():
    return 'welcome back'
@app.route('/webhook', methods=['GET', 'POST'])
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
    if req.get("result").get("action") != "pizza.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    variety = parameters.get("pizza-cost")

    cost = {'American':100, 'Indian':200, 'Mexican':300, 'Chinese':400}

    speech = "The cost of shipping to " + variety + " is " + str(cost[variety]) + " euros."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "messages": [
        {
          "type": 0,
          "speech": speech
        },
        {
          "type": 1,
          "platform": "telegram",
          "title": "Hi",
          "imageUrl": "https://www.apple.com/ac/structured-data/images/knowledge_graph_logo.png?201703170823",
          "buttons": [
          {
              "text": "Show me the Code",
              "postback": "http://www.grabon.in/coupon-codes/42672/"
            },
            {
              "text": "Know more",
              "postback": "Party"
            }
          ]
        }],
        "displayText": speech,
        "data": {},
        "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
