import json
import requests
import pandas as pd
import logging



logger = logging.getLogger(__name__)


class ServingClient:
    def __init__(self, ip: str = "0.0.0.0", port: int = 8088, features=None,keep_fts=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

        if features is None:
            features = ["distance"]
        self.features = features
        self.keep_fts = keep_fts

        # any other potential initialization

    def predict(self, X: pd.DataFrame,model:str) -> pd.DataFrame:
        """
        Formats the inputs into an appropriate payload for a POST request, and queries the
        prediction service. Retrieves the response from the server, and processes it back into a
        dataframe that corresponds index-wise to the input dataframe.
        
        Args:
            X (Dataframe): Input dataframe to submit to the prediction service.
        """

        json_post = json.loads(pd.DataFrame(X).to_json(orient="split"))
        json_post['model'] = model

        r = requests.post(
            f"{self.base_url}/predict", 
            json=json_post
        )    

        return r

        

    def logs(self) -> dict:
        """Get server logs"""

        r = requests.get(f"{self.base_url}/logs")  

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
            f"{self.base_url}/download_registry_model", 
            json=json_data
        )  

        return r.json() 
if __name__ == "__main__":

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

    sc = ServingClient(features=list_features,keep_fts=keep_fts)

    print(sc.predict(df_data))
    print(sc.logs())
    print(sc.download_registry_model(workspace='princesslove',model='question5-2-with-grid-search-json-model',version='1.0.0',source_experiment='question5.2-with-grid-search-json-model.json'))