import requests
import os
import json

class NHL_Season_Data_Fetcher:

    def __init__(self,seasons,out_dir):
        '''
        Initialise the Object
        self.seasons -> list of int ex:[2017,2018,2019]
        self.base_dir -> the directory where the jsons are or will be saved.
        '''
        self.seasons = seasons
        self.base_dir = out_dir

    def get_seasons(self) -> dict:
        '''
        Function that retrieves all data for all seasons and returns a dictionary.
        It returns a dictionary with a key for each year.
        '''
        d = dict()
        for year in self.seasons:
            d[year] = self.get_season(year)
        return d

    def get_season(self,year:int)->dict:
        '''
        Function that retrieves all data for a season.
        It returns a dictionary with two keys ['regular season','playoffs']
        '''

        assert(len(str(year))==4)

        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)

        season_out_dir = os.path.join(self.base_dir,str(year))
        if not os.path.exists(season_out_dir):
            os.mkdir(season_out_dir)

        dir_regular_season = os.path.join(season_out_dir,'regular_season')
        if not os.path.exists(dir_regular_season):
            os.mkdir(dir_regular_season)

        d = dict()

        d['regular season'] = self.get_regular_season(year,dir_regular_season)

        dir_playoffs = os.path.join(season_out_dir,'playoffs')

        if not os.path.exists(dir_playoffs):
            os.mkdir(dir_playoffs)

        d['playoffs'] = self.get_playoffs(year,dir_playoffs)

        return d




    def get_regular_season(self,year:int, out_dir:str) -> dict:
        '''
        Function that retrieves all data for each regular season game of a season.
        It returns a dictionary whose keys correspond to the Game ID of each game.
        '''
        number_of_games = 1230
        if year >= 2017:
            number_of_games = 1271
            
        if year == 2020:
            number_of_games = 868 # less matchs due to Covid

        d = dict()
        for game_number in range( 1 , number_of_games + 1 ):
            game_id = f'{year}02{game_number:04}'
            d[game_id] = self.get_game(game_id, out_dir)

        return d  


    def get_playoffs(self,year:int, out_dir:str) -> dict:
        '''
        Function that retrieves all data for each playoff game of a season.
        It returns a dictionary which keys correspond to the Game ID of each game.
        '''
        d = dict()
        nb_of_matchups_per_round = [8,4,2,1] # First round has 8 matchups, the second round has 4 matchups, etc.

        for round in range(1,5): # There are 4 rounds 

            for matchup in range(nb_of_matchups_per_round[round-1]): # Iterate through each matchup

                for match in range(1,8): # There are 7 games per matchup

                    game_id = f'{year}020{round}{matchup}{match}'
                    d[game_id] = self.get_game(game_id, out_dir)

        return d

    def get_game(self,game_id: int,out_dir:str) -> json:
        '''
        Function that retrieves the json file associated to a particular Game ID on
        https://statsapi.web.nhl.com/api/v1/game/[GAME_ID]/feed/live/
        It returns a json object.
        '''
        path = os.path.join(out_dir, game_id + '.json')
        
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)

        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live/'

        response = requests.get(url)
        
        with open(path,'+w') as f:
            f.write(response.text)

        return response.json


        



if __name__ == '__main__':

    path_out = os.path.join('datasets','raw')
    years = range(2016,2021)

    loader = NHL_Season_Data_Fetcher(years,path_out)
    d = loader.get_seasons()
