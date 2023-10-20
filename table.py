from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('table.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    data_input = request.form.get('data_input')
    # Process the data (e.g., parse JSON)
    try:
        data_dict = json.loads(data_input)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON input'})

    # Assuming data_dict is a list of dictionaries with the same keys
    table_data = data_dict

    return jsonify(table_data)



if __name__ == '__main__':
    app.run(debug=True)
