#!/usr/bin/python3
from flask import Flask
from flask import Response
import json
import http.client
import re

app = Flask(__name__)
@app.route("/metrics", methods=['GET'])
def index():
    conn = http.client.HTTPConnection('verahome.local', 3480, timeout=10)
    conn.request("GET","/data_request?id=sdata&output_format=text")
    res = conn.getresponse()
    #print(res.status, res.reason)
    data = res.read()
    #print(data)
    data_dict = json.loads(data)
    collect = ''
    for device_data in data_dict['devices']:
        for indiv_data in device_data.keys():
                key = 'device_' + re.sub("[^0-9a-zA-Z]+", "", str(device_data['name'])) + '_' + re.sub("[^0-9a-zA-Z]+", "", str(device_data['id'])) + '_' + re.sub("[^0-9a-zA-Z]+", "", indiv_data)
                collect += '# HELP ' + key + ' A super smart description goes here.\n'
                collect += '# TYPE ' + key + ' gauge\n'
                value = re.sub("[^0-9\.]+", "", str(device_data[indiv_data]))
                if(not(value and value.strip())):
                   collect += key + ' 0\n'
                else:
                   collect += key + ' ' + re.sub("[^0-9\.]+", "", str(device_data[indiv_data])) + '\n'

    return Response(collect, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='prometheus.local',port=9101)
