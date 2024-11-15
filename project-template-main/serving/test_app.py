from ift6758.models.utils import preprocess
import pandas as pd
import json
import requests



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
    X, Y ,_,_ =  preprocess(df_data,features = list_features, standarize=True,keep_fts = keep_fts)

    return X, Y

if __name__ == "__main__":

    r = requests.get(
        "http://127.0.0.1:8088/logs"
    )   

    print(r.json())
    print('Predict')
    X, Y = get_input_features_df()
    json_post = json.loads(pd.DataFrame(X).to_json(orient="split"))
    json_post['model'] = 'question5.3_grid_search_fts_selected.json'

    r = requests.post(
        "http://127.0.0.1:8088/predict", 
        json=json_post
    )    

    print(r.json())
    print(f'Accuracy {(Y==r.json()).mean()*100:.4}%')

    # json_data = {
    #     'workspace': 'princesslove',
    #     'model': 'question5-2-with-grid-search-json-model' ,
    #     'version' : '1.0.0',
    #     'source_experiment' : 'question5.2-with-grid-search-json-model.json.json',
    # }
    # r = requests.post(
    #     "http://127.0.0.1:8088/download_registry_model", 
    #     json=json_data
    # )  

    # print(r.json()) 
    
