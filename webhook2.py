#!/usr/bin/python3
import datetime
from flask import Flask, request, abort
from gevent.pywsgi import WSGIServer
import json
import vonage
import requests

client = vonage.Client(key='xxxxx', secret='xxxxx')

app = Flask(__name__)


@app.route('/inbound', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        json_str = json.dumps(request.json)
        resp = json.loads(json_str)
        # print(resp)
        json_from = resp['from']
        json_to = resp['to']
        if 'message_type' in resp:
           message_type = resp['message_type']
           if message_type == 'text':
               print('This is a text')
               if json_to == '14157386102':
                    print('This is a sandbox number')

                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    }
                    json_data = {
                        'from': '14157386102',
                        'to': resp['from'],
                        'message_type': 'text',
                        'text': 'Hi ' + resp['from'] + ' ,how are you? this is sandbox number',
                        'channel': 'whatsapp',
                    }
                    response = requests.post(
                        'https://messages-sandbox.nexmo.com/v1/messages',
                        headers=headers,
                        json=json_data,
                        auth=('xxxxx', 'xxxxx'),
                    )
               else:
                    if json_to == '6012xxxxx':
                        print('This is a production number')

                        headers = {
                        'Authorization': 'Bearer JWTxxxxxxxxxxxxxxgeneratedfromVONAGE', #https://developer.vonage.com/en/jwt
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        }

                        json_data = {
                        'message_type': 'text',
                        'text': 'Hi ' + resp['from'] + ' ,how are you? this is Production number',
                        'to': resp['from'],
                        'from': '6012xxxxx',
                        'channel': 'whatsapp',
                        }

                        response = requests.post(
                            'https://api.nexmo.com/v1/messages', headers=headers, json=json_data)

                        # Note: json_data will not be serialized by requests
                        # exactly as it was in the original request.
                        # data = '{\n"message_type": "text",\n"text": "i do not know, what say you?",\n"to": "6011xxxxxx",\n"from": "6012xxxxx",\n"channel":  "whatsapp"\n   }'
                        # response = requests.post('https://api.nexmo.com/v1/messages', headers=headers, data=data)

                    else:
                        print('')
           else:
               print('This is not a text')
           return 'success', 200
               # content = request.json()
               # target_to = content['to']
               # target_from = content['from']
               # print(target_from, target_to)

    else:
        abort(400)



@app.route('/status', methods=['POST'])
def webhook2():
    if request.method == 'POST':
        json_str = json.dumps(request.json)
        resp = json.loads(json_str)
        print(resp)
    return 'success', 200




if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8090)
    http_server = WSGIServer(('', 8090), app)
    http_server.serve_forever()
