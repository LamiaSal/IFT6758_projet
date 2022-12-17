import streamlit as st
import pandas as pd
import numpy as np
import requests,json
from ift6758.client.serving_game import ServingGame
from ift6758.client.serving_client import ServingClient
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

error =False
error_message = "error"
game = None
r= None
SG = ServingGame('streamingGames')
SC = ServingClient(features=list_features, keep_fts=keep_fts)


with st.sidebar:
    # TODO: Add input for the sidebar
    pick_workspace = st.sidebar.selectbox(
        "Workspace?",
        ('princesslove',)
    )

    pick_model = st.sidebar.selectbox(
        'Model',
        ('XGboost without features selection',
        'XGboost with features selection'
        )
    )

     # TODO: src experiment to be removed
    if pick_model == 'XGboost without features selection' : 
        model = 'question5-2-with-grid-search-json-model'
        src_exp = 'question5.2_with_grid_search.json' 
    elif pick_model == 'XGboost with features selection':
        model = 'question5-3-grid-search-fts-selected-model'
        src_exp = 'question5.3_grid_search_fts_selected.json' 
    else:
        error = True
        error_message = "the model does not exist"

    pick_version = st.sidebar.selectbox(
        'Version',
        ('1.0.0',
        )
    )

    download = st.button('Get Model')

    if download :
        SC.download_registry_model(workspace=pick_workspace, model=model, version=pick_version, source_experiment=src_exp)



with st.container():
    # TODO: Add Game ID input
    
    game_id = st.number_input('Game ID',value=2021020329)


    try :
        game = SG.getGame(game_id)
        team_home = game["team_home_name"].iloc[0]
        team_away = game["team_away_name"].iloc[0]
    except Exception as e :
        error = True
        error_message = "the game was not found"
    
    goals = [0,0]
    predict_goals = [0,0]
    if not error :
        try :
            X,Y,df_preprocessed,df_proc_flag = preprocess(game,features = list_features, standarize=True,keep_fts = keep_fts)
        except Exception as e :
            error = True
            error_message = "the game has not the necessary information for prediction"
    if not error :
        try :
            json_post = json.loads(pd.DataFrame(X).to_json(orient="split"))
            json_post['model'] = 'question5.3_grid_search_fts_selected.json'
            r = requests.post(
                "http://127.0.0.1:8088/predict", 
                json=json_post
            )
        except Exception as e :
            error = True
            error_message = "the prediction failed"
    if not error :
        try :
            for (index, row ) in game.iterrows():
                if row['result_event']=='Goal':
                    if row['name_team_that_shot'] == team_home:
                        goals[0]+=1
                    else:
                        goals[1]+=1
            
            for (index, row ), y in zip(df_proc_flag.iterrows(), r.json()[0]):
                if y == 1:
                    if row['name_team_that_shot'] == team_home:
                        predict_goals[0]+=1
                    else:
                        predict_goals[1]+=1

        except Exception as e :
            error = True
            error_message = "error in the computation of predicted and true number of goals per team"
    


with st.container():
    
    # TODO: Add Game info and predictions
    if not error :
        if st.button('Predict Game'):
            st.subheader(f'Game {game_id}:')
            team_away = game["team_away_name"].iloc[0]
            if (team_home == "Montréal Canadiens") or (team_away == "Canadiens") :
                st.balloons()
            st.subheader(f'{team_home} vs {team_away}')
            st.text(f'perdiod A FAIRE - A FAIRE left')
            #st.text(f'{team_away} {predict_goals[1]}({goals[1]})')
            c1, c2 = st.columns(2)
            c1.metric(label=f'{team_home} xG (actual)', value=f'{predict_goals[0]}({goals[0]})', delta=f'{predict_goals[0]-goals[0]}',
            delta_color="off")
            c2.metric(label=f'{team_away} xG (actual)', value=f'{predict_goals[1]}({goals[1]})', delta=f'{predict_goals[1]-goals[1]}',
            delta_color="off")
            
            df = pd.DataFrame(X,columns=df_preprocessed.columns)
            df['Prediction proba']=r.json()[1]
            df['Prediction']=r.json()[0]
            df['Truth'] = Y.astype('int')
            st.dataframe(df)
        else:
            st.write('Waiting on button press...')
    else :
        st.text(error_message)
    
with st.container():
    # TODO: Add data used for predictions
    pass
