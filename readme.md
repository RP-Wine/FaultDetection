# File content
```
FaultDetection/
├── data/
    ├── battery_brand1/                 #datasets
    ├── battery_brand2/
    ├── battery_brand3/
    └── five_fold_train_test_split.ipynb#for spliting the dataset for five-fold cross-validation
├── DyAD/                               # core scripts related to the DyAD model
    ├── dyad_vae_save/                  # saved models and results
        └── 2024-12-31-17-33-32_fold0/
            ├── model/                  # saved trained model 
            |── result/                 # saved results  
            |── feature/                # extracted features from train set
            |── loss/                   # loss plots
            └── mean/                   # segment scores mean
    ├── model/                          # model definitions
        ├── dataset.py                  # data loder
        ├── dynamic_vae.py              # core model scripts
        └── tasks.py                    # task allocater
    ├── evaluate.py                     # for evaluating trained models
    ├── extract.py                      # for feature extraction 
    ├── main_five_fold.py               # entrance for training with five-fold cross-validation
    ├── model_params_battery_brand1.json# model parameters
    ├── ... (other parameter files)
    ├── params_fivefold.json            # parameters for five-fold cross-validation
    ├── train.py                        # training scripts
    └── utils.py                        # utility functions
├── ngrok                               # for connecing server to the internet
├── output/                             # directory for output files used by the server
    ├── car_score/
    ├── current/
    ├── max_single_volt/
    ├── max_temp/
    ├── min_single_volt/
    ├── segment_score/
    ├── soc/
    └── volt/
├── jsonfier.py                         # for reconstruting the needed data
├── robust_scores.py                    # for robust score calculation 
├── score.py                            # functions for server to reconstruct the score datas
└── server.py                           # server
```
# For first run:
## Basic requirements
```
# basic environment
CUDA 10.2  # Must use this specific version. Please follow https://developer.nvidia.com/cuda-10.2-download-archive. 
python 3.6

# pytorch version
pytorch==1.5.1

# run after installing correct Pytorch package
pip install --no-index torch-scatter -f https://pytorch-geometric.com/whl/torch-1.5.0+cu102.html
pip install --no-index torch-sparse -f https://pytorch-geometric.com/whl/torch-1.5.0+cu102.html
pip install --no-index torch-cluster -f https://pytorch-geometric.com/whl/torch-1.5.0+cu102.html
pip install --no-index torch-spline-conv -f https://pytorch-geometric.com/whl/torch-1.5.0+cu102.html
pip install torch-geometric==1.5.0
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
pip install tensorflow==2.6.2
```
## Generating five-fold datasets
run the `five_fold_train_test_split.ipynb` to split the datasets

## Training the model
using scripts from DyAD team to train the model
```
cd DyAD
python main_five_fold.py --config_path model_params_battery_brand1.json --fold_num 0
```

## Generating robust scores
after training, generate the robust scores of the cars by running `robust_scores.py`

## Generating the needed segment datas 
currently the needed data can only be reconstruted before running the server because it costs a lot of time and cannot be done quick enough when the user is interacting with the interface.
run `jsonfier.py` to reconstruct the datas needed by the server
# Establishing the server
## Running the local server
run the local server `server.py`, and a local server will be established on your pc
## Connecting the local server to the internet
use ngrok to connect the server to the internet, for detailed information, visit: https://ngrok.cc/

# User interface
connect to the following URL: https://charts.thingjs.com/kunpeng/preview/publish/ZJja6z

# Code Reference
Scripts used in DyAD folder are partly from the following github repo:
```
https://github.com/962086838/Battery_fault_detection_NC_github
```
ngrok uesed in this project is from Sunny-Ngrok:
```
https://ngrok.cc/
```