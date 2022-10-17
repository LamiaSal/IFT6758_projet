'''
This code can also be found in the jupyternotebook named "tusying_data" in the notebooks directory
'''
import pandas as pd
import json
from os import listdir
from os.path import isfile, join

def get_generalData(data):
    '''
    this function take as entry :
        - data : a json file data (corresponding to one match)
    it returns the general metadata of the match:
        - [id_game,season,dateTime,endDateTime,abstractGameState,team_away_name,team_home_name]
    '''
    id_game = data['gameData']['game']['pk']
    season = data['gameData']['game']['season']
    try :
        dateTime =  data['gameData']['datetime']['dateTime']
    except :
        #print(f"dateTime not found for match {id_game}")
        dateTime = None
    try :
        endDateTime = data['gameData']['datetime']['endDateTime']
    except :
        #print(f"endDateTime not found for match {id_game}")
        endDateTime = None
    
    abstractGameState = data['gameData']['status']['abstractGameState']
    team_away_name = data['gameData']['teams']['away']['name']
    team_home_name = data['gameData']['teams']['home']['name']
    return [id_game,season,dateTime,endDateTime,abstractGameState,team_away_name,team_home_name]

def get_file_event_rows_data(data,type_season):
    ''' 
    this function take as entry :
        - data : a json file data (corresponding to one match of season defined by type_season)
        - type_season : the season in format 20XX20XX (for instance 20162017)
    It ouputs the a list of list, in which each row contains metadata of one event of the match (only shots and goals are considered)
    the metadata the following :
        -  columns_name = [
            "event_Idx","period", "periodTime","id_team_that_shot","name_team_that_shot","result_event","x_coord","y_coord",\
                "rinkSide_of_the_team_that_shot","goalie_name",\
                "shooter_name","shot_type","empty_net","strength",\
                "type_season","id_game","season","dateTime","endDateTime","abstractGameState","team_away_name","team_home_name"]
    '''
    match_data = get_generalData(data)
    team_away_name,team_home_name = match_data[-2],match_data[-1]
    match_events_list = []
    for item in data['liveData']['plays']['allPlays']:
        if item['result']['event'] not in ["Goal", "Shot"]:
            continue
        else :
            # event Idx
            event_Idx = item['about']['eventIdx']

            # period
            period = item['about']['period']

            # periodTime
            periodTime = item['about']['periodTime']
            
            # team information (which team shot)
            id_team_that_shot = item['team']['id'] 
            name_team_that_shot = item['team']['name'] 

            # indicator if its a shot or a goal
            result_event = item['result']['event']
            
            # the on ice coordinates
            try :
                x_coord = item['coordinates']['x'] 
                y_coord = item['coordinates']['y']
            except :
                #print(f"coordinates not found for match {match_data[-7]} and event {event_Idx}")
                x_coord = None
                y_coord = None

            # the rinkside of the the_team_that_shot
            try : 
                # sometimes we don't have the info on the rinksidee apparently
                if team_away_name == name_team_that_shot :
                    if int(period)%2==0:
                        # in case of prolongation even (knowing that the max prolongation in the history is 6)
                        rinkSide_of_the_team_that_shot = data['liveData']['linescore']['periods'][1]['away']['rinkSide']
                    else :
                         # in case of prolongation odd
                        rinkSide_of_the_team_that_shot = data['liveData']['linescore']['periods'][0]['away']['rinkSide']
                else :
                    if int(period)%2==0:
                        rinkSide_of_the_team_that_shot = data['liveData']['linescore']['periods'][1]['home']['rinkSide']
                    else : 
                        rinkSide_of_the_team_that_shot = data['liveData']['linescore']['periods'][0]['home']['rinkSide']
            except Exception as e :
                #print(e)
                #print(f"period not defined for match {match_data[-7]} and event {event_Idx} and period:{period}")
                rinkSide_of_the_team_that_shot = None


            # the shooter and goalie name
            goalie_name = None
            shooter_name = None
            for item_bis in item['players']:
                if item_bis['playerType']=="Goalie":
                    goalie_name = item_bis['player']["fullName"]
                elif item_bis['playerType'] in ["Shooter", "Scorer"]:
                    shooter_name = item_bis['player']["fullName"]
                else:
                    continue
            '''
            if goalie_name == None :
                print(f"goalie_name not found for match {match_data[-7]} and event {event_Idx}")
            if shooter_name == None :
                print(f"shooter_name  not found for match {match_data[-7]} and event {event_Idx}")
            '''
            # shot type
            try :
                shot_type = item['result']['secondaryType']
            except :
                # sometimes the secondary Type is not defined
                #print(f"shot_type not found for match {match_data[-7]} and event {event_Idx}")
                shot_type = None

            try : 
                # empty net
                empty_net = item['result']['emptyNet']
            except :
                empty_net = None

            
            # strength
            try :
                strength = item['result']['name']
            except :
                strength = None
            
            all_data = [event_Idx, period, periodTime, id_team_that_shot,name_team_that_shot,result_event,x_coord,y_coord,rinkSide_of_the_team_that_shot,goalie_name,shooter_name,shot_type,empty_net,strength]
            match_events_list.append(all_data+[type_season]+match_data)
    return match_events_list

if __name__ == '__main__':

    # list all the json files extracted in datasets
    dir_year = [ join("../datasets/raw/", d_y) for d_y in listdir("../datasets/raw/")]
    dir_pl_reg = [(join(path, d_pl_reg),d_pl_reg)  for path in dir_year for d_pl_reg in listdir(path)  ]
    fichiers = [(join(dir_path, f),d_pl_reg) for (dir_path, d_pl_reg) in dir_pl_reg\
        for f in listdir(dir_path) if isfile(join(dir_path, f))]
    

    # extract all metedata 
    all_list_data = []
    for (file_name_path, type_season) in fichiers :
        with open(file_name_path,'r') as f:
            # load json data of the match
            data = json.loads(f.read())
            
            if 'messageNumber' in data and data['messageNumber'] == 2:
                continue
            
            all_list_data = all_list_data + get_file_event_rows_data(data,type_season)
    
    # transform into a dataframe
    columns_name = [
    "event_Idx","period", "periodTime","id_team_that_shot","name_team_that_shot","result_event","x_coord","y_coord","rinkSide_of_the_team_that_shot","goalie_name",\
            "shooter_name","shot_type","empty_net","strength",\
            "type_season","id_game","season","dateTime","endDateTime","abstractGameState","team_away_name","team_home_name"]
    df = pd.DataFrame(all_list_data, columns=columns_name)

    # save in datasets directory
    df.to_csv("../datasets/tidy_data.csv", index=False)