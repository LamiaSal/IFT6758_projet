import streamlit as st
import pandas as pd
import datetime, os
import datetime

from ift6758.client.serving_game import ServingGame
from ift6758.client.serving_client import ServingClient
from ift6758.models.utils import preprocess
from dotenv import load_dotenv
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
load_dotenv()
SG = ServingGame('streamingGames')
IP = os.environ.get("SERVING_IP", "127.0.0.1")
PORT = os.environ.get("SERVING_PORT", "8088")
DEBUG = os.environ.get("DEBUG", False)

timeFormat = "%M:%S"
hasPredictions = False

class GameInfo():
    def __init__(self,game_id,isLive):
        self.game_id= game_id
        self.isLive = isLive
        self.goals = [0,0]
    def setInfo(self,game:pd.DataFrame):
        self.team_home = game["team_home_name"].iloc[0]
        self.team_away = game["team_away_name"].iloc[0]
        if self.isLive:
            self.livePeriod = game['period'].max()
            PERIOD_END = datetime.datetime.strptime("20:00", timeFormat)
            self.liveTimeLeft = PERIOD_END - datetime.datetime.strptime(game[game['period']==self.livePeriod]['periodTime'].max(),timeFormat)

        for (_, row ) in game.iterrows():
            if row['result_event']=='Goal':
                if row['name_team_that_shot'] == self.team_home:
                    self.goals[0]+=1
                else:
                    self.goals[1]+=1



with st.sidebar:
    if DEBUG:
        ip = st.text_input('IP',value=IP)
        port = st.text_input('Port',value=PORT)
        SC = ServingClient(ip= ip,port = port,features=list_features, keep_fts=keep_fts)
    else:
        SC = ServingClient(ip= IP,port = PORT,features=list_features, keep_fts=keep_fts)

    pick_workspace = st.sidebar.selectbox( "Workspace?",('princesslove',))

    pick_model = st.sidebar.selectbox('Model',('XGboost with features selection','XGboost without features selection'))

    pick_version = st.sidebar.selectbox('Version',('1.0.0',))

    

    if pick_model == 'XGboost without features selection' : 
        model = 'question5-2-with-grid-search-json-model'
        src_exp = 'question5.2_with_grid_search.json.json' 
    elif pick_model == 'XGboost with features selection':
        model = 'question5-3-grid-search-fts-selected-model'
        src_exp = 'question5.3_grid_search_fts_selected.json' 

    download = st.button('Get Model')
    if download and not error:
        with st.spinner('Wait for it...'):
            SC.download_registry_model(workspace=pick_workspace, model=model, version=pick_version, source_experiment=src_exp)
            st.success('Done!')
        
        


with st.container():
    # TODO: Add Game ID input
   
    game_id = st.number_input('Game ID',value=2022020525)
    (game, isLive) ,status= SG.getGame(game_id)
    try :
       
        if status == False:
            error = True
            error_message = 'This is not a valid game ID.'
        else:
            gameInfo = GameInfo(game_id,isLive)
            gameInfo.setInfo(game)
        if isLive:
            path  = f'predictions/{pick_model}/{game_id}.csv'
            if os.path.exists(path):
                hasPredictions = True
                predictions = pd.read_csv(path)
                
                cond = game['event_Idx'].isin(predictions['event_Idx'])
                game.drop(game[cond].index, inplace = True)
           
    except Exception as e :
        error = True
        error_message = "The game was not found."

    
   
    
    if not error :
        
        try :
            if not game.empty:
                X,Y,df_preprocessed,df_proc_flag = preprocess(game, features = list_features, standarize=True, keep_fts = keep_fts)
                print('X',X)
        except Exception as e :

            error = True
            error_message = "the game has not the necessary information for prediction"
    
    
 
    if not error and len(X)!=0:
        try :
            new_predictions = SC.predict(X,src_exp).json()
            
            if "Model don't exists!" in new_predictions:
                error = True
                error_message= "You didn't download this model. Click on Get Model..."
        except Exception as e :
            error = True
            error_message = e
   
    if not error:
       
        if not game.empty and len(X)!= 0:
            new_df = pd.DataFrame(X,columns=df_preprocessed.columns)
            new_df['Prediction proba']=new_predictions[1]
            new_df['Prediction']=new_predictions[0]
            new_df['Truth'] = Y.astype('int')
            new_df['event_Idx'] = df_proc_flag['event_Idx']
            new_df['name_team_that_shot'] = df_proc_flag['name_team_that_shot']
            

            cols = list(new_df.columns)
            cols = cols[-2:] + cols[:-2]
            new_df = new_df[cols]
        
            if isLive and hasPredictions:
                predictions = pd.concat([predictions, new_df],ignore_index = True)
            else:
                predictions = new_df
        

    if not error :
        predict_goals = [0,0]
        proba_goals = [0.0,0.0]
        try:
            for _,row in predictions.iterrows():
                if row['Prediction'] == 1:
                    if row['name_team_that_shot'] == gameInfo.team_home:
                        predict_goals[0]+=1
                    else:
                        predict_goals[1]+=1
                if row['Prediction proba']>0.5:
                    if row['name_team_that_shot'] == gameInfo.team_home:
                        proba_goals[0] += row['Prediction proba']
                    else:
                        proba_goals[1] += row['Prediction proba']


        except Exception as e :
            error = True
            error_message = "error in the computation of predicted and true number of goals per team"
        


with st.container():
   
    # TODO: Add Game info and predictions
    if not error :
        if st.button('Ping Game'):
            st.subheader(f'Game {game_id}:')
            team_away = game["team_away_name"].iloc[0]
            if (gameInfo.team_home == "Montréal Canadiens") or (team_away == "Canadiens") :
                st.balloons()
            st.subheader(f'{gameInfo.team_home} vs {team_away}')
            if isLive:
                st.text(f'Live Game')
            
                st.text(f'Period {gameInfo.livePeriod} - Time left {str(gameInfo.liveTimeLeft)[2:]}')
            
            c1, c2 = st.columns(2)
            c1.metric(label=f'{gameInfo.team_home} xG (actual)', value=f'{proba_goals[0]:.1f}({gameInfo.goals[0]})', delta=f'{proba_goals[0]-gameInfo.goals[0]:.1f}',
            delta_color="off")
            c2.metric(label=f'{team_away} xG (actual)', value=f'{proba_goals[1]:.1f}({gameInfo.goals[1]})', delta=f'{proba_goals[1]-gameInfo.goals[1]:.1f}',
            delta_color="off")
            
           
           
           
            
            st.dataframe(predictions)
            out_path  = os.path.join('predictions',pick_model)
            if not os.path.exists(out_path) :
                os.makedirs(out_path)
            
            predictions.to_csv(os.path.join(out_path,f'{game_id}.csv'),index=False)
        else:
            st.write('Waiting on button press...')
    else :
        st.text(error_message)
    

