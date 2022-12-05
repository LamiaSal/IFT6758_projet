
import sys
import os
import ift6758
from ift6758.models.utils import download_model,preprocess
from CometMLClient import download_model_with_exception
import pandas as pd
import json
import requests
from ift6758.models.utils import preprocess, predict_model,download_model, compute_metrics
from xgboost import XGBClassifier

def get_input_features_df():
    
    df_data = pd.read_csv('Datasets/df_test.csv')

    # question 5
    list_features = ['empty_net', 'periodTime','period', 'x_coord', 'y_coord','distance','angle','shot_type',\
        'last_event_type', 'last_x_coord', 'last_y_coord','distance_from_last', 'seconds_since_last', \
            'rebound', 'angle_change','speed']


    keep_fts = ['empty_net','periodTime','period','x_coord','y_coord','distance','angle',\
    'last_x_coord','last_y_coord','distance_from_last','seconds_since_last',\
    'rebound','angle_change','speed','shot_type_Backhand',\
    'shot_type_Deflected','shot_type_Slap Shot','shot_type_Snap Shot',\
    'shot_type_Tip-In','shot_type_Wrap-around','shot_type_Wrist Shot',\
    'last_event_type_Blocked Shot','last_event_type_Faceoff',\
    'last_event_type_Giveaway','last_event_type_Goal','last_event_type_Hit',\
    'last_event_type_Missed Shot','last_event_type_Penalty',\
    'last_event_type_Takeaway']

    # preprocess
    X, Y ,df_preprocessed,_ =  preprocess(df_data,features = list_features, standarize=True,keep_fts = keep_fts)

    return X, Y

if __name__ == "__main__":
   
    X, Y = get_input_features_df()
    json_post = json.loads(pd.DataFrame(X).to_json(orient="split"))
    json_post['model'] = 'question5.3_grid_search_fts_selected.json'

    r = requests.post(
        "http://127.0.0.1:8088/predict", 
        json=json_post
    )
    

    print(r.json())
    print(f'Accuracy {(Y==r.json()).mean()*100:.4}%')
