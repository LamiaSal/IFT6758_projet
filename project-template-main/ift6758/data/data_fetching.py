import requests
import os

def get_season(year: int, out_dir:str):

    assert(len(str(year))==4)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    out_dir = os.path.join(out_dir,str(year))
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    dir_regular_season = os.path.join(out_dir,'regular_season')
    if not os.path.exists(dir_regular_season):
        os.mkdir(dir_regular_season)

    get_regular_season(year,dir_regular_season)

    dir_playoffs = os.path.join(out_dir,'playoffs')

    if not os.path.exists(dir_playoffs):
        os.mkdir(dir_playoffs)

    get_playoffs(year,dir_playoffs)



def get_game(game_id: int,out_dir:str):

    path = os.path.join(out_dir, game_id + '.json')
    if os.path.exists(path):
        return

    url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live/'

    response = requests.get(url)
    
    with open(path,'+w') as f:
        f.write(response.text)

def get_regular_season(year:int, out_dir:str):

    number_of_games = 1230
    if year >= 2017:
        number_of_games = 1271
        
    if year == 2020:
        number_of_games = 868 # less matchs due to Covid

    for game_number in range( 1 , number_of_games + 1 ):
        game_id = f'{year}02{game_number:04}'
        get_game(game_id, out_dir)
        


def get_playoffs(year:int, out_dir:str):
    
    matchups = [8,4,2,1]
    for round in range(1,5): # There is 4 rounds 
        for matchup in range(matchups[round-1]):
            for match in range(1,8): # There is 7 matchs
                game_id = f'{year}020{round}{matchup}{match}'
                get_game(game_id, out_dir)




    



if __name__ == '__main__':
    for year in range(2016,2021):
        get_season(year,os.path.join('datasets','raw'))