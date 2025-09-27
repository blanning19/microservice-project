from flask import Flask, request
import csv
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        filename = "/etc/data/" + data["file"]
        product = data["product"]

        incorrect_format = {
            "file": data["file"],
            "error": "Input file not in CSV format."
        }

        try:
            with open(filename, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                sum = 0
                for row in csv_reader:
                    if len(row) < 2:
                        return json.dumps(incorrect_format), 400
                    if row[0] == product:
                        try:
                            sum += int(row[1])
                        except ValueError:

                            return json.dumps(incorrect_format), 400
                if sum == 0:
                    return json.dumps(incorrect_format), 400
                else:
                    return json.dumps({"file": data["file"], "sum": sum})
        except Exception as e:

            return json.dumps(incorrect_format), 400

    else:
        return "You are now in the second container"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5002)











