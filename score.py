import torch
import os
import numpy as np
import json


def get_segment_scores(car_num, segment_num):
    file_name = f"output/segment_score/{car_num}_{segment_num}.json"
    run_folder = 'DyAD/dyad_vae_save/2024-12-31-17-33-32_fold0/' 
    # target numbers:
    target_car_number = car_num # car number
    target_segment_number = segment_num # segment number
    feature_dir = os.path.join(run_folder, 'mean')
    found = False
    target_rec_error = None
    #serch lists:
    file_list = [f for f in os.listdir(feature_dir) if f.endswith('_label.file')]
    for filename in file_list:
        file_path = os.path.join(feature_dir, filename)       
        #load the dict
        batch_metadata = torch.load(file_path)
        #the specific datas
        cars = batch_metadata.get('car', np.array([])) 
        segments = batch_metadata.get('charge_segment', []) 
        rec_errors = batch_metadata.get('rec_error', []) 

        #finding
        for i in range(len(cars)):
            current_car = cars[i].item() 
            current_segment = int(segments[i]) 
            #print(type(current_car))
            if current_car == target_car_number and current_segment == target_segment_number:
                target_rec_error = rec_errors[i]
                found = True
                #print(f"\nat {filename} and {i} found")
                break 
        if found:
            break 
    # output
    if found:
        print("Segment Score:", target_rec_error)
        result = {
            'x':"Segment Score",
            'y':target_rec_error,
            's':1
        }
        with open(file_name, 'w') as f:
            json.dump(result,f,indent=4)


def get_robust_score(car_num):
    file_name = f"output/car_score/{car_num}.json"
    score_file_path = 'DyAD/auc/car_scores.npy' 
    all_scores = np.load(score_file_path,allow_pickle=True).item()
    #print(all_scores)
    result = {
        'content':all_scores[car_num]
    }
    with open(file_name, 'w') as f:
        json.dump(result,f,indent=4)

