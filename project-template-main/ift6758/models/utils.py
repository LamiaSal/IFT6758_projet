from datetime import datetime as dt
from datetime import timedelta 
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
from comet_ml import Experiment
import os
from ift6758.models.plotter import *
from comet_ml import API



def save_metrics_and_models_on_comet(model,y_val,y_val_pred,y_val_prob,model_names,model_dir,name_experiment, register_model = True):
    load_dotenv()
    
    experiment = Experiment(
            api_key=os.environ.get('COMET_API_KEY'),
            project_name='itf-6758-team-4',
            workspace='princesslove',
        )
    experiment.set_name(name_experiment)

    # save and log model
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

def predict_model(model,X_val):
    # predict on validation set
    y_val_pred = model.predict(X_val)
    y_val_prob = model.predict_proba(X_val)
    return y_val_pred,y_val_prob[:,1]

def convert_to_float(X):
    if X == "Goal":
        return 1.0
    else:
        return 0.0
def convert_to_total_seconds(X):
    t_ = dt.strptime(X, '%M:%S')
    delta = timedelta(minutes=t_.minute,seconds=t_.second)
    return delta.total_seconds()

def preprocess(df, features,standarize=False):
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
    df_proc = df_proc.dropna()

    # define Y (the target)
    Y = df_proc['result_event']

    # Select features
    df_proc = df_proc[features]

    # convert periodTime in seconds
    if 'periodTime' in features:
        df_proc['periodTime']=df_proc['periodTime'].apply(convert_to_total_seconds)
    
    # one hot encoding of the shot_type
    if 'shot_type' in features:
        df_proc['shot_type'] = df_proc['shot_type'].dropna()
        df_proc = pd.get_dummies(df_proc,columns=['shot_type'])    
    
    # one hot encoding of the last_event_type
    if 'last_event_type' in features:
        df_proc = pd.get_dummies(df_proc,columns=['last_event_type'])
    
    # define X and standardize it
    X = df_proc
    if standarize:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    return X, Y.values,df_proc