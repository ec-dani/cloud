from flask import Flask, request, jsonify
from pymongo import MongoClient
#Para correr el mongo en el container lo hicimos asi. 
#docker run -d --name mongodb -p 27017:27017 -v mongodemo:/data/db  mongo
#Si da porblemas puede ser porque el puerto 27017 esta siendo usado, entonces termina el proceso que lo esta usando.

app = Flask(__name__)

#client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb://mongodb:27017/')
db = client['iot_data_db']
collection = db['sensor_data']

@app.route('/api/store_data', methods=['POST'])
def store_data():
    data = request.json
    try:
        collection.insert_one(data)
        print(f'Data: ',data)
        return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/find', methods=['GET'] )
def find():
    try:
        data = list(collection.find({}))
        print(f'Data: ',data)
        return jsonify({'message': 'Data ok'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
