import sys
import os
import ift6758
from ift6758.models.utils import download_model,preprocess
import pandas as pd

def download_model_with_exception(json):
    # TODO regler le problemes des noms

    # input
    register_name = json['model']#'question5-3-grid-search-fts-selected-model' 
    package_path = ift6758.__path__
    # boolean if the model you are querying for is already downloaded
    mode_downloaded = os.path.exists(os.path.join(package_path,'comet_models', register_name))

    if mode_downloaded :
        # load that model
        download_model(register_name, workspace = json['workspace'],version = json['version'],output_path=mode_downloaded)
        # write to the log about the model change.  
        info = f"model updated {json}"
    else :
        try : 
            #try downloading the model:
            download_model(register_name, workspace = json['workspace'],version = json['version'],output_path=mode_downloaded)
            info = f"model downloaded {json}"
        except Exception as e :
            # write to the log about the failure
            info = e
    
    return info
    '''
    experiment_name = 'question5.3_grid_search_fts_selected'
    download_model(register_name = register_name )

    model_xgb_without_RDS = XGBClassifier()
    model_xgb_without_RDS.load_model(os.path.join("comet_models",experiment_name,".json"))
    '''
