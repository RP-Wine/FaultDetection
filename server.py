from flask import Flask, jsonify, request
import json
import jsonfier as loader
import score
app = Flask(__name__)


def get_file(data_type, car_num, segment):
    file_path = f'output/{data_type}/{car_num}_{segment}.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": f"File {file_path} not found"}), 404

@app.route('/')
def hello():
    return "hello"

@app.route('/segment',methods=['POST'])
def return_segment_scores():
    data = request.get_json()
    car_num = int(data.get('car_num'))
    segment = int(data.get('segment'))
    file_name = f"output/segment_score/{car_num}_{segment}.json"
    score.get_segment_scores(car_num,segment)
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/car',methods=['POST'])
def return_car_scores():
    data = request.get_json()
    car_num = int(data.get('car_num'))
    file_name = f"output/car_score/{car_num}.json"
    score.get_robust_score(car_num)
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/', methods=['POST'])
def return_segment():
    try:
        data = request.get_json()        
        car_num = data.get('car_num')
        segment = data.get('segment')
        data_type = data.get('type')#'volt','current','soc','max_single_volt','max_temp'
        #print(data)
        #loader.read_car_data(car_num)
        if not segment:
            return jsonify({"error": "Missing 'segment' in JSON data"}), 400
        
        return get_file(data_type, car_num, segment)
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid JSON data"}), 400


if __name__ == '__main__':
    app.run(debug=True)