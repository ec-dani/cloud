from flask import Flask, render_template
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['iot_data_db']
collection = db['sensor_data']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_data')
def show_data():
    data = list(collection.find({}))
    return render_template('show_data.html', data=data)

@app.route('/graph')
def graph():
    sensor_data = collection.find({})

    sensor_data_dict = {}
    for data in sensor_data:
        sensor_id = data['sensor_id']
        if sensor_id not in sensor_data_dict:
            sensor_data_dict[sensor_id] = {'humans_detected': [], 'unknown_detected': []}
        sensor_data_dict[sensor_id]['humans_detected'].append(data['humans_detected'])
        sensor_data_dict[sensor_id]['unknown_detected'].append(data['unknown_detected'])

    sensor_graph_data = []
    for sensor_id, data in sensor_data_dict.items():
        humans_detected = sum(data['humans_detected'])
        unknown_detected = sum(data['unknown_detected'])
        average_humans_detected = humans_detected / len(data['humans_detected']) if data['humans_detected'] else 0
        average_unknown_detected = unknown_detected / len(data['unknown_detected']) if data['unknown_detected'] else 0
        sensor_graph_data.append({'sensor_id': sensor_id, 'humans_detected': humans_detected, 'unknown_detected': unknown_detected, 'average_humans_detected': average_humans_detected, 'average_unknown_detected': average_unknown_detected} )

    return render_template('graph.html', sensor_graph_data=json.dumps(sensor_graph_data))

@app.route('/average_hd')
def average_hd():
    pipeline = [{
        "$group": {
            "_id": None,
            "average": {"$avg":"$humans_detected"}
        }
    }]
    average = list(collection.aggregate(pipeline))[0]["average"]
    return render_template('average_hd.html', average=average)


@app.route('/max_uhd')
def min_max():
    pipeline = [
        {"$group": {
            "_id": "$sensor_id",
            "max_uhd": {"$max": "$unknown_detected"}
        }}
    ]
    data = list(collection.aggregate(pipeline))
    return render_template('max.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001 , debug=True, ssl_context=("myCert.pem", "myKey.pem"))
