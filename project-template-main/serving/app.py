"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:
    
    $ gunicorn --bind 0.0.0.0:<PORT> app:app
gunicorn can be installed via:
    $ pip install gunicorn
"""
import os
from pathlib import Path
import logging
from flask import Flask, jsonify, request, abort
import sklearn
import pandas as pd
import joblib
from CometMLClient import download_model_with_exception
from ift6758.models.utils import preprocess, predict_model,download_model, compute_metrics
from xgboost import XGBClassifier

import ift6758


LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")


app = Flask(__name__)
logging.basicConfig(filename='flask.log',level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 


@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e.g. load model,
    setup logging handler, etc.)
    """
    # TODO: setup basic logging configuration
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    
    # TODO: any other initialization before the first request (e.g. load default model)
    json_data = {
        'workspace': 'princesslove',
        'model': 'question5-3-grid-search-fts-selected-model' ,
        'version' : '1.0.0',
        'source_experiment' : 'question5.3_grid_search_fts_selected.json',
    }

    response = download_model_with_exception(json_data)

    app.logger.info(response)


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    
    # TODO: read the log file specified and return the data
    with open('flask.log') as f:
        text = f.read()

    response = text
    return jsonify(response)  # response must be json serializable!


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model
    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.
    Recommend (but not required) json with the schema:
        {
            workspace: (required),
            model: (required),
            version: (required),
            ... (other fields if needed) ...
        }
    
    """
    # Get POST json data
    json_data = request.get_json()
    app.logger.info(json_data)

    # TODO
    response = download_model_with_exception(json_data)

    app.logger.info(response)
    return jsonify(response)  # response must be json serializable!



@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict
    Returns predictions
    """
    # Get POST json data
    json_data = request.get_json()    
   
    package_path = os.path.abspath(os.path.join(ift6758.__path__[0], '..'))


    model = json_data['model']
    models_dir  = os.path.join(package_path,'comet_models')

    model_xgb_without_RDS = XGBClassifier()

    if os.path.exists(os.path.join(models_dir,model)):
        try :
            model_xgb_without_RDS.load_model(os.path.join(models_dir,model))
            data = json_data['data']
            y_test_pred_XGB, _ = predict_model(model_xgb_without_RDS,data)
            response = y_test_pred_XGB

        except Exception as e :
            print('error in prediction',e)
            response = e
            app.logger.info(e)
    else:
       message = "Model don't exists!" 
       app.logger.info(message) 
       response = message
    
    

    app.logger.info(response)
    return jsonify(response.tolist())  # response must be json serializable!