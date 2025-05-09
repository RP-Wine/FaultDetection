from flask import Flask, jsonify, request
import json
import jsonfier as loader
import score
app = Flask(__name__)

#get the segment datas
def get_file(data_type, car_num, segment):
    file_path = f'output/{data_type}/{car_num}_{segment}.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": f"File {file_path} not found"}), 404
    
#simple test API
@app.route('/')
def hello():
    return "hello"

#send segment scores
@app.route('/segment',methods=['POST'])
def return_segment_scores():
    #get the required params
    data = request.get_json()
    car_num = int(data.get('car_num'))
    segment = int(data.get('segment'))

    #search and reconstruct the data
    file_name = f"output/segment_score/{car_num}_{segment}.json"
    score.get_segment_scores(car_num,segment)

    #return the data
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

#send car scores
@app.route('/car',methods=['POST'])
def return_car_scores():
    #get the required params
    data = request.get_json()
    car_num = int(data.get('car_num'))

    #search and reconstruct the data
    file_name = f"output/car_score/{car_num}.json"
    score.get_robust_score(car_num)

    #return the data
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

#send segment datas
@app.route('/', methods=['POST'])
def return_segment():

    #get the required params
    data = request.get_json()        
    car_num = data.get('car_num')
    segment = data.get('segment')
    data_type = data.get('type') #'volt','current','soc','max_single_volt','max_temp'

    #currently due to long execution time, the following script has a low performance:
    '''
    loader.read_car_data(car_num)
    '''

    if not segment:
        return jsonify({"error": "Missing 'segment' in JSON data"}), 400    
    return get_file(data_type, car_num, segment)



if __name__ == '__main__':
    app.run(debug=True)