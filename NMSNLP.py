# -*- coding: UTF-8 -*-
import urllib3
import requests
import json
import os
import ssl
from flask import Flask, request, make_response, jsonify
import sys
import inspect
import pprint
from onms_client import *
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Check if all environment variables are set

BOT_ACCESS_TOKEN = 'MGIyZWJhNGUtMDhkNy00ZThlLWE4ZjMtZGM2MWU1ZTdhNTNjZjc5N2M5ZmEtOGM1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
BOT_ID = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS84NjA1ZGZkMS04MmVmLTRiMDQtOGE1My05Y2MxZjQ0ZGY3OTk"

app = Flask(__name__)
urllib3.disable_warnings()

URL = "https://api.ciscospark.com/v1/messages"

# Use the following in case your variables are in a different sub-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dirParent = os.path.dirname(currentdir)
dirVariable = dirParent
sys.path.insert(0, dirVariable)

HEADERS_bot = {"Content-type": "application/json; charset=utf-8",
               "Authorization": "Bearer " + BOT_ACCESS_TOKEN}

EMEAR = 'EMEAR-SE.cisco.com'
SEBOT = 'sebot.cisco.com'
GlobalSE = 'se.cisco.com'

file = open("authorized_list.txt", "r")


# webhook received from Spark:
@app.route('/', methods=['GET', 'POST'])
def indix():
    action = None
    req = request.get_json(force=True)
    #print("\n")
    ssl._create_default_https_context = ssl._create_unverified_context
    # fetch info from json
    action = req.get('queryResult').get('intent').get('displayName')
    roomId = req.get('originalDetectIntentRequest').get('payload').get('data').get('data').get('roomId')
    person = req.get('originalDetectIntentRequest').get('payload').get('data').get('data').get('personEmail')
    #pprint.pprint(person)
    client = onms_client()
    file.seek(0)
    authorized = file.read()
    if person not in authorized:
        send_message("you are not authorized", roomId)
    elif action == "check_status":
        vmname = req.get('queryResult').get('parameters').get('vm_name')
        if vmname == EMEAR:
            toprint = output(0, client, vmname)
            sendingOutput(toprint, roomId, vmname, 0, client)
        if vmname == SEBOT:
            toprint = output(1, client, vmname)
            sendingOutput(toprint, roomId, vmname, 1, client)
        if vmname == GlobalSE:
            toprint = output(2, client, vmname)
            sendingOutput(toprint, roomId, vmname, 2, client)
        if vmname == 'all':
            sendingOutputAll(client, roomId)
        #send_message(toprint, room_id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

def output(id, client, vmname):
    status = client.get_vm_status(id)
    latency = client.get_wan_latency()
    httplatency = client.get_vm_http_latency(id)
    name = client.get_vm_name(id)
    toprint = "The status of {} VM is:\n".format(name)
    toprint = toprint + "{0:15}{1:30}\n".format('Status', 'Protocol')
    for key, value in status.items():
        if value == "up":
            toprint = toprint + "{0:15}{1:30}\n".format('✅', key)
        else:
            toprint = toprint + "{0:15}{1:30}\n".format('❌', key)
    toprint = toprint + "BDLK-Dubai ICMP Response Time is {}\n".format(latency)
    toprint = toprint + "HTTP response time for {} is {}\n".format(vmname, httplatency)
    toprint = toprint + "For more  information click here http://nms.cisco.com:8980"
    return toprint


def sendingOutput(toprint, roomId, vmname, id, client):
    send_message(toprint, roomId)
    client.onms_graph_return_wan()
    client.onms_graph_return_http(id)
    send_icmp(roomId)
    send_http(roomId, vmname)

def sendingOutputAll(client, roomId):
    toprint = output(0, client, EMEAR) + "\n\n"
    toprint = toprint + output(1, client, SEBOT) + "\n\n"
    toprint = toprint + output(2, client, GlobalSE)
    toprint = toprint + "\n\nAlso to check the status for more VMs visit http://nms.cisco.com:8980"
    send_message(toprint, roomId)

    client.onms_graph_return_wan()
    send_icmp(roomId)

    client.onms_graph_return_http(0)
    send_http(roomId, EMEAR)

    client.onms_graph_return_http(1)
    send_http(roomId, SEBOT)

    client.onms_graph_return_http(2)
    send_http(roomId, GlobalSE)



# create a route for webhook
def webhook():
    # return response
    return make_response(jsonify(results()))




def send_icmp(room_id):
    m = MultipartEncoder({'roomId': room_id,
                          'text': 'BDLK-Dubai ICMP Response Time',
                          'files': ('icmp.png', open('icmp.png', 'rb'),
                                    'image/png')})
    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                      headers={'Authorization': 'Bearer '+ BOT_ACCESS_TOKEN,
                               'Content-Type': m.content_type})

def send_http(room_id, vmname):
    m = MultipartEncoder({'roomId': room_id,
                          'text': 'HTTP Response Time for {}'.format(vmname),
                          'files': ('http.png', open('http.png', 'rb'),
                                    'image/png')})
    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                      headers={'Authorization': 'Bearer ' + BOT_ACCESS_TOKEN,
                               'Content-Type': m.content_type})

def send_message(msg, room_id):
    msg = {"text": msg, "roomId": room_id}
    requests.post("https://api.ciscospark.com/v1/messages", data=json.dumps(msg), headers=HEADERS_bot)

    #requests.post("https://api.ciscospark.com/v1/messages", data=m, headers=HEADERS_bot)



# for deployment in heroku:
# host is 0.0.0.0
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port " + str(port))
    app.run(debug=False, port=port, host='127.0.0.1', threaded=True)

