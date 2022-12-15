import streamlit as st
import pandas as pd
import numpy as np
import requests,json
from ift6758.client.serving_game import ServingGame
from ift6758.models.utils import preprocess
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
st.title("NHL goal predictor")

game = None
r= None
SG = ServingGame('')

with st.sidebar:
    # TODO: Add input for the sidebar
    pick_workspace = st.text_input('Workspace:', 'princesslove')
    pick_model = st.text_input('Model', 'question5-3-grid-search-fts-selected-model')
    pick_version = st.text_input('Version:', '1.0.0')
    
    download = st.button('Get Model')   


with st.container():
    # TODO: Add Game ID input
    game_id = st.number_input('Game ID',2021020329)
    pingged = st.button('Ping Game')

    game = SG.getGame(game_id)
    team_home = game["team_home_name"].iloc[0]
    team_away = game["team_away_name"].iloc[0]
    goals = [0,0]
    predict_goals = [0,0]
    

    
    X,Y,df_preprocessed,_ = preprocess(game,features = list_features, standarize=True,keep_fts = keep_fts)

    

    json_post = json.loads(pd.DataFrame(X).to_json(orient="split"))
    json_post['model'] = 'question5.3_grid_search_fts_selected.json'
    r = requests.post(
	    "http://127.0.0.1:8088/predict", 
	    json=json_post
    )
    
    for (index, row), y in zip(game.iterrows(),r.json()):
        if row['result_event']=='Goal':
            if row['name_team_that_shot'] == team_home:
                goals[0]+=1
            else:
                goals[1]+=1
        if y == 1:
            if row['name_team_that_shot'] == team_home:
                predict_goals[0]+=1
            else:
                predict_goals[1]+=1





    

with st.container():
    # TODO: Add Game info and predictions
    st.subheader(f'Game {game_id}:')
    st.subheader(f'{team_home} vs {game["team_away_name"].iloc[0]}')
    st.text(f'{team_home} {predict_goals[0]}({goals[0]})')
    st.text(f'{team_away} {predict_goals[1]}({goals[1]})')
    
    df = pd.DataFrame(X,columns=df_preprocessed.columns)
    df['Prediction']=r.json()
    df['Truth'] = Y.astype('int')
    st.dataframe(df)
    
with st.container():
    # TODO: Add data used for predictions
    pass
