'''
This code can also be found in the jupyternotebook named "tusying_data" in the notebooks directory
'''

from comet_ml import Experiment
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import os

if __name__ == '__main__':
    print(os.environ.get('COMET_API_KEY'))
    experiment = Experiment(
        api_key=os.environ.get('COMET_API_KEY'),
        project_name='itf-6758-team-4',
        workspace='princesslove',
    )
    

    url = 'https://drive.google.com/file/d/1kM__riNHRPx5GsyuOH3yhiql3OZvwmuP/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    
    
    

    subset_df = df[df['id_game']== 2017021065]
    print(subset_df)

    
    experiment.log_dataframe_profile(
    subset_df, 
    name='wpg_v_wsh_2017021065',  # keep this name
    dataframe_format='csv'  # ensure you set this flag!
    )
    