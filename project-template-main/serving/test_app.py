
import sys
import os
import ift6758
from ift6758.models.utils import download_model,preprocess
import pandas as pd
import json
import requests

def get_input_features_df():
    
    df_data = pd.read_csv('df_test.csv')

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
    print(ift6758.__path__)
    print("YOOOO")
    r = requests.post(
        "http://0.0.0.0:8088/predict", 
        json=json.loads(pd.DataFrame(X).to_json())
    )
    print("YOOOO")
    print(r.json())
