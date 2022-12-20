import pandas as pd
import logging
import os, requests
from ift6758.tidying_data.advanced_tidying_data import * 
import ift6758

logger = logging.getLogger(__name__)

def download_game(game_id: int, out_dir:str) -> str:
        '''
        Function that retrieves the json file associated to a particular Game ID at
        https://statsapi.web.nhl.com/api/v1/game/[GAME_ID]/feed/live/
        It returns a json object.
        '''
        path = os.path.join(out_dir, str(game_id) + '.json')
        
        if os.path.exists(path):
            with open(path) as f:
                return path

        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live/'

        response = requests.get(url)
        
        with open(path,'+w') as f:
            f.write(response.text)

        return path

class ServingGame():
    def __init__(self,outDir) -> None:
        self.outDir = os.path.join(os.path.dirname(ift6758.__path__[0]), 'datasets', outDir)

        if not os.path.exists(self.outDir ) :
            os.mkdir(self.outDir )
            

    def getGame(self,gameID:int)->pd.DataFrame:
        path = download_game(gameID,self.outDir)

        return get_game_events(path, 'regular_season')


if __name__ =='__main__':
    sg = ServingGame('streamingGames')
    df ,isLive= sg.getGame(2022020486)
    print("Is Live:",isLive)
    print(df.head())

    

        
