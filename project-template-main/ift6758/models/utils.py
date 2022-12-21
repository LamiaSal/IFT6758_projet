from datetime import datetime as dt
from datetime import timedelta 
import pandas as pd
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
from comet_ml import Experiment
import os
from ift6758.models.plotter import *
from comet_ml import API
import pickle

SHOT_TYPES = ['shot_type_Backhand',
       'shot_type_Deflected', 'shot_type_Slap Shot', 'shot_type_Snap Shot',
       'shot_type_Tip-In', 'shot_type_Wrap-around', 'shot_type_Wrist Shot']

LAST_EVENT_TYPES = ['last_event_type_Blocked Shot', 'last_event_type_Faceoff',
       'last_event_type_Giveaway', 'last_event_type_Goal',
       'last_event_type_Hit', 'last_event_type_Missed Shot',
       'last_event_type_Penalty', 'last_event_type_Shot',
       'last_event_type_Takeaway']

COlUMNS_ORDER = ['empty_net', 'periodTime', 'period', 'x_coord', 'y_coord',
       'distance', 'angle', 'last_x_coord', 'last_y_coord',
       'distance_from_last', 'seconds_since_last', 'rebound',
       'angle_change', 'speed', 'powerplay','team_that_shot_nb','other_team_nb',
       
       'shot_type_Backhand','shot_type_Deflected', 'shot_type_Slap Shot',
       'shot_type_Snap Shot', 'shot_type_Tip-In', 'shot_type_Wrap-around',
       'shot_type_Wrist Shot',
       
       'last_event_type_Blocked Shot', 'last_event_type_Faceoff', 'last_event_type_Giveaway',
       'last_event_type_Goal', 'last_event_type_Hit',
       'last_event_type_Missed Shot', 'last_event_type_Penalty',
       'last_event_type_Shot', 'last_event_type_Takeaway']

def preprocess(df, features,standarize=False, drop_fts = [], keep_fts = []):
    df_proc = df.copy()

    # convert target into readable content for the models
    df_proc['result_event']=df_proc['result_event'].apply(convert_to_float)
    
    # fille empty net nan by False
    df_proc["empty_net"].fillna(False,inplace=True)

    # convert boolean data in 0 and 1
    df_proc["empty_net"]=df_proc["empty_net"].map({True:1,False:0})
    df_proc["rebound"]=df_proc["rebound"].map({True:1,False:0})
    
    # fill strength nan by 0 values
    df_proc["strength"].fillna(0.0,inplace=True)
    
    # Select features
    df_proc = df_proc[[*features,*['name_team_that_shot'], *['result_event']]]
    df_proc = df_proc.dropna()
    
    # define Y (the target)
    Y = df_proc['result_event']
    df_proc = df_proc.drop(['result_event'], axis = 1)
    

    # convert periodTime in seconds
    if 'periodTime' in features:
        df_proc['periodTime']=df_proc['periodTime'].apply(convert_to_total_seconds)
    
    # one hot encoding of the shot_type
    if 'shot_type' in features:
        df_proc['shot_type'] = df_proc['shot_type'].dropna()
        df_proc = pd.get_dummies(df_proc,columns=['shot_type'])   

        # check if all shot types expected have been withdraw
        for shot_type in SHOT_TYPES :
            if shot_type not in df_proc.columns :
                # if in the incoming dataset, shot type is lacking, then we add a column with only zeros
                df_proc[shot_type]=0 
    
    
    # one hot encoding of the last_event_type
    if 'last_event_type' in features:
        df_proc = pd.get_dummies(df_proc,columns=['last_event_type'])

        # check if all events types expected have been withdraw
        for event_type in LAST_EVENT_TYPES :
            if event_type not in df_proc.columns :
                df_proc[event_type]=0
    

    df_proc_flag = df_proc.copy()
    order_selected_fts = [ft for ft in COlUMNS_ORDER if ft in df_proc.columns]
    df_proc = df_proc[order_selected_fts]

    # drop features specified by drop_fts
    if len(drop_fts) >= 1:
        df_proc = df_proc.drop(drop_fts, axis=1)
    
    # select keep_fts features
    if len(keep_fts) >= 1:
        df_proc = df_proc[keep_fts]
    
    # define X and standardize it
    X = df_proc
    if standarize:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    return X, Y.values,df_proc.reset_index(drop=True),df_proc_flag

def save_metrics_and_models_on_comet(model,y_val,y_val_pred,y_val_prob,model_names,model_dir,name_experiment, register_model = True, sklearn_model=False):
    load_dotenv()
    
    experiment = Experiment(
            api_key=os.environ.get('COMET_API_KEY'),
            project_name='itf-6758-team-4',
            workspace='princesslove',
        )
    experiment.set_name(name_experiment)

   
    if not os.path.exists(f'../models_config/{model_dir}'):
        os.makedirs(f'../models_config/{model_dir}')
    # save and log model
    if sklearn_model:
        pkl_filename = f'../models_config/{model_dir}/{name_experiment}.pkl'
        with open(pkl_filename, 'wb+') as file:
            pickle.dump(model, file)
        experiment.log_model(f"{name_experiment}_Model", pkl_filename)
    else :
        model.save_model(f'../models_config/{model_dir}/{name_experiment}.json')
        experiment.log_model(f"{name_experiment}_Model", f'../models_config/{model_dir}/{name_experiment}.json')

    # log data and finish experiment
    log_All(y_val,y_val_pred,y_val_prob,model_names,experiment)

    # if you want to register the model
    if register_model :
        # Register model
        api = API()

        experiment = api.get(f"princesslove/itf-6758-team-4/{name_experiment}")
        experiment.register_model(f"{name_experiment}_Model")

    experiment.end()


def download_model(register_name, workspace = "princesslove",version = "1.0.0",output_path="../comet_models/"):
    load_dotenv()
    api = API()
    # Download a Registry Model:
    api.download_registry_model(workspace, f"{register_name}", version,
                                output_path=output_path, expand=True)

def predict_model(model,X_val):
    # predict on validation set
    y_val_pred = model.predict(X_val)
    y_val_prob = model.predict_proba(X_val)
    return y_val_pred,y_val_prob[:,1]

def compute_metrics(y_true,y_preds,model_names):
    acc=[]
    recall = []
    precision = []
    f_score = []
    auc = []
    for y_pred, model_name in zip(y_preds, model_names):
        acc.append(metrics.accuracy_score(y_true,y_pred))
        recall.append(metrics.recall_score(y_true,y_pred,average='macro'))
        precision.append(metrics.precision_score(y_true,y_pred,average='macro'))
        f_score.append(metrics.f1_score(y_true,y_pred,average='macro'))
        fpr, tpr, _ = metrics.roc_curve(y_true, y_pred)
        auc.append(metrics.auc(fpr, tpr))

    dict_data = {
    'model_name':model_names,
    'Accuracy':acc,
    'Recall':recall,
    'Precision':precision,
    'f_score':f_score,
    'AUC':auc
    }
    return pd.DataFrame.from_dict(dict_data)

def convert_to_float(X):
    if X == "Goal":
        return 1.0
    else:
        return 0.0
def convert_to_total_seconds(X):
    t_ = dt.strptime(X, '%M:%S')
    delta = timedelta(minutes=t_.minute,seconds=t_.second)
    return delta.total_seconds()


