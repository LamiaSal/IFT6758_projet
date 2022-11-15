from datetime import datetime as dt
from datetime import timedelta 
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

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