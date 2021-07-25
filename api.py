from fastapi import FastAPI
import json
# from flask import request, jsonify

App = FastAPI()
#App.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
def open_file():
    with open('input.json') as json_data:
        return json.load(json_data)
    #print(credit_refs)

@App.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@App.route('/api/credit_refs/all', methods=['GET'])
def api_all():
    credit_refs=open_file()
    return jsonify(credit_refs)


@App.route('/api/credit_refs', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    credit_refs=open_file()
    for credit_ref in credit_refs:
        if credit_ref['id'] == id:
            results.append(credit_ref)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

App.run()