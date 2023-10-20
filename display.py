from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
import requests
import json

app = Flask(__name__, template_folder = 'templates') 


def table(locations_list):

    # Add backslashes and double quotes to each element

    print(locations_list)
    #output_string = ', '.join(['\\"' + item + '\\"' for item in locations_list])
    output_string = ', '.join(locations_list)
    burp0_url = "https://mgmresorts.logscale.us-2.crowdstrike.com:443/api/v1/repositories/2023edw/query/"
    burp0_headers = {"Authorization": "bearer SPVO5jlbcJODBc8s2jVB7wytC2wfkEWg~NrQqGmpYVNYEi5HGUu45OzSBgcTOrXBkO5AhYysQrqaR", "Content-Type": "application/json"}
    #burp0_json={"end": "now", "queryString":f"Country=CA | in(\"Original State\",values=[MB])" ,"start": 0}
    burp0_json={"end": "now", "queryString":"Country=CA | in(\"Original State\",values=[" + output_string +  "])" ,"start": 0}
    burp1_json={"end": "now", "queryString":"Country=CA | in(\"Original State\",values=[" + 'BC, NB' + "])" ,"start": 0}

    result = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    print(burp0_json)
    print(result)
    resp = result.content
    json_data = resp.decode('utf-8')
    table_object = []
    for value in json_data.split('\n'):
        if value != "":
            table_object.append(json.loads(value))

    return table_object


def territories(file_name):
    with open(file_name) as f:
        location = f.read().splitlines()
    return [{"value":territoy, "text":territoy} for territoy in location]


@app.route('/') 
def index(): 
    return render_template('index.html', canada=territories('locations/Canada'), us_states=territories('locations/US')) #, table_object=process_selection()) 

'''
@app.route('/table', methods=['POST', 'GET'])
def table():
    burp0_url = "https://mgmresorts.logscale.us-2.crowdstrike.com:443/api/v1/repositories/2023edw/query/"
    burp0_headers = {"Authorization": "bearer SPVO5jlbcJODBc8s2jVB7wytC2wfkEWg~NrQqGmpYVNYEi5HGUu45OzSBgcTOrXBkO5AhYysQrqaR", "Content-Type": "application/json"}
    
    process_selection_result = process_selection()  # Get the list of selected states
    print(process_selection()) 
    formatted_states = ['| "Original State"= "{}"'.format(state) for state in process_selection_result]
    original_state = ''.join(formatted_states)    
    print(original_state) 
    burp0_json={"end": "now", "queryString":f"Country=CA | {original_state}","start": 0}
    
    result = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    resp = result.content
    json_data = resp.decode('utf-8')
    table_object = []
    for value in json_data.split('\n'):
        if value != "":
            table_object.append(json.loads(value))

    return render_template('table.html', data=table_object)
'''


@app.route('/process_selection', methods=['POST'])
def process_selection():
    selected_territories = request.form.getlist('selected_territories')  # Get the list of selected territories
    json_objects = []
    for item in selected_territories:
        # Remove the single quotes and convert to a dictionary
        item_dict = json.loads(item.replace("'", "\""))
        json_objects.append(item_dict['text'])

    table_object = table(json_objects)
    return render_template('table.html', table_object=table_object)
    #return table_object


@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        lisc = request.form['license']
        ssn = request.form['ssn']

    burp0_url = "https://mgmresorts.logscale.us-2.crowdstrike.com:443/api/v1/repositories/2023edw/query/"
    burp0_headers = {"Authorization": "bearer SPVO5jlbcJODBc8s2jVB7wytC2wfkEWg~NrQqGmpYVNYEi5HGUu45OzSBgcTOrXBkO5AhYysQrqaR", "Content-Type": "application/json"}
    burp0_json={"end": "now", "queryString":f"driver_license ={lisc}" ,"start": 0}
    #burp0_json={"end": "now", "queryString":"Country=CA | \"Original State\"=BC","start": 0}
    
    result = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

    resp = result.content
    print(resp)    
    return resp



if __name__ == '__main__':
    app.run(debug=True)