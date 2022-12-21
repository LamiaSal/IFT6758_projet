import pandas as pd
import logging
import os, requests
from ift6758.tidying_data.advanced_tidying_data import * 


logger = logging.getLogger(__name__)

def download_game(game_id: int, path:str) -> str:
        '''
        Function that retrieves the json file associated to a particular Game ID at
        https://statsapi.web.nhl.com/api/v1/game/[GAME_ID]/feed/live/
        It returns a json object.
        '''

        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live/'

        response = requests.get(url)
        if response.status_code != 200:
            return False

        with open(path,'+w') as f:
            f.write(response.text)

        return True

class ServingGame():
    def __init__(self,outDir) -> None:
        self.outDir = os.path.join('datasets', outDir)

        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir )
            

    def getGame(self,gameID:int)->pd.DataFrame:
        path = os.path.join(self.outDir, str(gameID) + '.json')
        if not os.path.exists(path):
            if not download_game(gameID,path):
                return (False, False), False
        return get_game_events(path, 'regular_season'), True

        


if __name__ =='__main__':
    sg = ServingGame('streamingGames')
    df ,isLive, state= sg.getGame(2022020501)
    print("Is Live:",isLive)
    print(df.head())

    

        
