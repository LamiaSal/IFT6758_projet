import os
from ift6758.models.utils import download_model


def download_model_with_exception(json):
    # input
    register_name = json['model'] #'question5-3-grid-search-fts-selected-model' 
    # package_path = os.path.abspath(os.path.dirname(os.path.join(ift6758.__path__[0])))

    # models_dir  = os.path.join(package_path,'comet_models')
    models_dir = 'comet_models'
    if not os.path.exists(models_dir) :
        print("do not exist")
        os.mkdir(models_dir)


    model_downloaded = os.path.join(models_dir, json['source_experiment'])
    
    if os.path.exists(model_downloaded) and os.path.isfile(model_downloaded) :
        info = f"model already downloaded"
    else :
        #try downloading the model:
        try:
            download_model(register_name, workspace = json['workspace'],version = json['version'],output_path=models_dir)
            info = f"model downloaded"  
        except:
            info = f'failed to download model'  
               
    return info
   

if __name__ == "__main__":
    json_data = {
        'workspace': 'princesslove',
        'model': 'question5-3-grid-search-fts-selected-model' ,
        'version' : '1.0.0',
        'source_experiment' : 'question5.3_grid_search_fts_selected.json',
    }
    download_model_with_exception(json_data)
