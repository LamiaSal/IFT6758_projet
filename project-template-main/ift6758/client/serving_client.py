import json
import requests
import pandas as pd
import logging
from ift6758.models.utils import preprocess


logger = logging.getLogger(__name__)


class ServingClient:
    def __init__(self, ip: str = "127.0.0.1", port: int = 8088, features=None,keep_fts=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

        if features is None:
            features = ["distance"]
        self.features = features
        self.keep_fts = keep_fts

        # any other potential initialization

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the inputs into an appropriate payload for a POST request, and queries the
        prediction service. Retrieves the response from the server, and processes it back into a
        dataframe that corresponds index-wise to the input dataframe.
        
        Args:
            X (Dataframe): Input dataframe to submit to the prediction service.
        """

        # preprocess
        X, _,_,_ =  preprocess(X,features = self.features, standarize=True, keep_fts = self.keep_fts)

        json_post = json.loads(pd.DataFrame(X).to_json(orient="split"))
        json_post['model'] = 'question5.3_grid_search_fts_selected.json'

        r = requests.post(
            "http://127.0.0.1:8088/predict", 
            json=json_post
        )    

        return r.json()

        

    def logs(self) -> dict:
        """Get server logs"""

        r = requests.post(f"{self.base_url}/log")  

        return r.json()

    def download_registry_model(self, workspace: str, model: str, version: str,source_experiment:str) -> dict:
        """
        Triggers a "model swap" in the service; the workspace, model, and model version are
        specified and the service looks for this model in the model registry and tries to
        download it. 
        See more here:
            https://www.comet.ml/docs/python-sdk/API/#apidownload_registry_model
        
        Args:
            workspace (str): The Comet ML workspace
            model (str): The model in the Comet ML registry to download
            version (str): The model version to download
        """

        json_data = {
            'workspace': workspace,
            'model': model ,
            'version' : version,
            'source_experiment' : source_experiment
        }
        r = requests.post(
            "http://127.0.0.1:8088/download_registry_model", 
            json=json_data
        )  

        return r.json() 