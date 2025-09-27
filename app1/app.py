from flask import Flask, request
import os
import requests
import json

app = Flask(__name__)

@app.route('/')
@app.route('/calculate', methods=['POST', 'GET'])
# walahy el 3azeem 3ashh ya amar
def index():

    if request.method == 'POST':
        data = request.get_json()

        file = data["file"]


        # Error message
        invalid_json = {
            "file": None,
            "error": "Invalid JSON input."
        }
        # Joke is on you thi should be in app2, bas we will see it at the end.

        incorrect_path = {
            "file": file,
            "error": "File not found."
        }

        # Validation checks
        if file == None:
            return json.dumps(invalid_json)
        else:
            filee = file.split(".")
            filepath = "/etc/data/" + file

            if not os.path.exists(filepath):
                return json.dumps(incorrect_path)
            else:
                response = requests.post('http://app2:5002/', json=data)
                return response.json()
    else:
        return "You are in the calculate endpoint now"


if __name__ == '__main__':
    app.debug = True
    # for I will make it 5001, and then change it to 6000, once I submit it
    app.run(host='0.0.0.0', port=6000)

