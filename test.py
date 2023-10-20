from flask import Flask, render_template, request, make_response, jsonify
import requests
import json

burp0_url = "https://mgmresorts.logscale.us-2.crowdstrike.com:443/api/v1/repositories/2023edw/query/"
burp0_headers = {"Authorization": "bearer SPVO5jlbcJODBc8s2jVB7wytC2wfkEWg~NrQqGmpYVNYEi5HGUu45OzSBgcTOrXBkO5AhYysQrqaR", "Content-Type": "application/json"}
burp0_json={"end": "now", "queryString":"Country=CA | \"Original State\"=MB","start": 0}

result = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
resp = result.content
json_data = resp.decode('utf-8')
json_object = []
for value in json_data.split('\n'):
    if value != "":
        json_object.append(json.loads(value))

print(json_object)
    
