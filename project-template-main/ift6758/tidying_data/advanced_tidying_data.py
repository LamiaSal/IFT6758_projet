import pandas as pd
import json


import datetime
from datetime import timedelta
from math import sqrt
import numpy as np


def get_generalData(data):
    '''
    this function take as entry :
        - data : a json file data (corresponding to one match)
    it returns the general metadata of the match:
        - [id_game,season,team_away_name,team_home_name]
    '''
    id_game = data['gameData']['game']['pk']
#     season = data['gameData']['game']['season']
    yearBegin = str(id_game)[:4]
    season = yearBegin + str(int(yearBegin) + 1)
    
    team_away_name = data['gameData']['teams']['away']['name']
    team_home_name = data['gameData']['teams']['home']['name']
    return [id_game,season,team_away_name,team_home_name]

timeFormat = "%M:%S"
PERIOD_START = datetime.datetime.strptime("00:00", timeFormat)
PERIOD_END = datetime.datetime.strptime("20:00", timeFormat)

class PlayerOnBench:
    def __init__(self,name,team,penalty):
        self.name = name
        self.team = team
        self.penalty = penalty
        self.penalties_types = [penalty.type]
             
    def add_penalty(self,penalty):
        if self.penalty.add_penalty(penalty):
            self.penalties_types.append(penalty.type)
            # self.penalty.print_()
        else:
            self.penalty = penalty
            self.penalties = [penalty.type]
        
        
    def remove_penalty(self,periodTime,period):
        currentTime = datetime.datetime.strptime(periodTime, timeFormat)
        if self.penalty.time_left(periodTime,period) > timedelta(minutes=2):
            if period == self.penalty.period_ends:
                self.penalty.end -= timedelta(minutes=2)
                return False
            else:
                t3 = datetime.datetime.strptime("02:00", timeFormat)
                if currentTime - timedelta(minutes=2) < PERIOD_START:
                    self.penalty.period_ends -= 1
                    self.penalty.end = PERIOD_END - (t3 - self.penalty.end)
                return False
        else:
            # print('\033[92m\nPenalty over because GOAL')
            # self.penalty.print_()
            return True
                        
    def isOnBench(self,time,period):
        return self.penalty.isin(time,period)
        
        
class Penalty:
    def __init__(self,item):
        
        self.ID = item['about']['eventIdx']
        self.team = item['team']['name']
        for item_bis in item['players']:
            if item_bis['playerType']=="PenaltyOn":
                self.player = item_bis['player']["fullName"]
                break

        self.type = item['result']['penaltySeverity']

        
        self.start = datetime.datetime.strptime(item['about']['periodTime'], timeFormat)
        self.duration =item['result']['penaltyMinutes']
        self.end = self.start + timedelta(minutes=self.duration)
        
        self.period_start = item['about']['period'] 
        self.period_ends = self.period_start
        
        if self.end > PERIOD_END:
            self.period_ends = self.period_start + 1
            self.end = self.end - timedelta(minutes=20) 
        
        # self.print_()
       
    def print_(self):
        print()
        print(self.start,self.period_start)
        print('Player:',self.player,'\nTeam:',self.team,'\nSeverity:',self.type)
        print(self.end,self.period_ends)
        print()
        
    def add_penalty(self,new_penalty):
        # print(self.start,new_penalty.start)
        if (new_penalty.start - self.start).total_seconds()<15 :
            # print('Combine Penlaties')
            self.end += timedelta(minutes=new_penalty.duration)
            
            if self.end > datetime.datetime.strptime("20:00", timeFormat):
                self.period_ends = self.period_start + 1
                self.end = self.end - timedelta(minutes=20) 
            return True
        # print('Dont combine')
        return False
    def time_left(self,periodTime,period):
        
        currentTime = datetime.datetime.strptime(periodTime, timeFormat)
        if period == self.period_ends:
            return self.end - currentTime
        else:
            return (PERIOD_END - currentTime) + (self.end - PERIOD_START) 
        
    def isin(self,currentTime,period):
        currentTime = datetime.datetime.strptime(currentTime, timeFormat)
        if period == self.period_ends and currentTime <= self.end:
            return True
        if period  == self.period_ends - 1 and currentTime >= self.start:
            return True
        
        return False
        
            
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
    previous_event = None
    
    playersOnBench = []
    nb_player_home = 5
    nb_player_away = 5
    score = [0,0]
    
    for item in data['liveData']['plays']['allPlays']:
        if item['result']['event'] == 'Penalty':
            # print(f'\033[91m')
            p = Penalty(item)
            if p.type == "Misconduct":
                pass
                # print("Misconduct")
            else:
                playerIsOnBench = False
                for player in playersOnBench:
                    if player.name == p.player:
                        player.add_penalty(p)
                        playerIsOnBench = True
                        break
                if not playerIsOnBench:
                    if p.team == team_away_name and nb_player_away > 3:
                        player = PlayerOnBench(p.player,p.team,p)
                        playersOnBench.append(player)
                        nb_player_away -= 1
                    if p.team == team_home_name and nb_player_home > 3:
                        player = PlayerOnBench(p.player,p.team,p)
                        playersOnBench.append(player)
                        nb_player_home -= 1
            
        if item['result']['event'] not in ["Goal", "Shot"]:
            previous_event = item
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
            
            current_team_nb = 5
            other_team_nb = 5
            isPenalty = False
            isPenaltyOver = False
            for i in range(len(playersOnBench)-1,-1,-1):
                if playersOnBench[i].isOnBench(periodTime,period):
                    isPenalty = True                    
                else:
                    # print('\033[92m\nPenalty over')
                    # print(periodTime)
                    isPenaltyOver = True
                    # playersOnBench[i].penalty.print_()
                    if playersOnBench[i].team == team_away_name:
                        nb_player_away += 1
                    else:
                        nb_player_home += 1
                    playersOnBench.pop(i)
                    
            powerPlay = 0      
             
            if isPenalty or isPenaltyOver:
                # print(f'Home Team {nb_player_home} vs {nb_player_away}')
                if name_team_that_shot == team_away_name:
                    current_team_nb = nb_player_away
                    other_team_nb = nb_player_home
                else:
                    current_team_nb = nb_player_home
                    other_team_nb = nb_player_away
                if current_team_nb > other_team_nb:
                    # print(f'Power Play')
                    powerPlay = 1
                    if result_event == "Goal":
                        idx = -1
                        minT = datetime.datetime.now()
                        for i in range(len(playersOnBench)):
                            if playersOnBench[i].team != name_team_that_shot:
                                if 'Minor' in playersOnBench[i].penalties_types:
                                    if playersOnBench[i].penalty.end < minT:
                                        minT = playersOnBench[i].penalty.end
                                        idx = i
                        if idx != -1:
                            if playersOnBench[i].remove_penalty(periodTime,period):
                                if playersOnBench[idx].team == team_away_name:
                                    nb_player_away += 1
                                else:
                                    nb_player_home += 1
                                playersOnBench.pop(idx)
                                # print(f'Home Team {nb_player_home} vs {nb_player_away}')
                            
            
           
            
            if result_event == "Goal":
                # print('Goal!')
                if name_team_that_shot == team_away_name:
                    score[1]+=1
                else:
                    score[0]+=1
                # print(f'Home {score[0]}:{score[1]} Away')
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
            
            # the on ice coordinates
            try :
                x_coord = item['coordinates']['x'] 
                y_coord = item['coordinates']['y']         
            except :
                #print(f"coordinates not found for match {match_data[-7]} and event {event_Idx}")
                x_coord = None
                y_coord = None
            
            
             
            try:   
                if rinkSide_of_the_team_that_shot == 'left':
                    distance_from_net =  sqrt((90 - x_coord)**2 + (y_coord-0)**2)
                    angle  = np.arcsin(y_coord/distance_from_net)
                else:
                    distance_from_net =  sqrt((-90 - x_coord)**2 + (y_coord-0)**2)
                    angle  = -np.arcsin(y_coord/distance_from_net)
            except:
                distance_from_net = None
                angle = None

           
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
                strength = item['result']['strength']['name']
            except :
                strength = None
                
            ### PREVIOUS EVENT ###
            # Default values
            rebond = False
            last_x_coord = None
            last_y_coord = None
            distance_from_last_event = None
            speed = None
            change_in_angle = 0
            time_since_last_event = None
            last_event_type = None
            
            if period != previous_event['about']['period']:
                previous_event = None
                
            if previous_event :
                
                # Last event type
                last_event_type = previous_event['result']['event']
                
                # Is rebound
                if last_event_type in ["Goal", "Shot"]:
                    rebond = True

                # time since last event
                dt_time = datetime.datetime.strptime(periodTime, "%M:%S")
                dt_last_time = datetime.datetime.strptime(previous_event['about']['periodTime'], "%M:%S")
                time_since_last_event = (dt_time - dt_last_time).total_seconds()  
                if time_since_last_event == 0:
                    time_since_last_event = 0.5
                    
               
                try :
                    # the on ice coordinates
                    last_x_coord = previous_event['coordinates']['x'] 
                    last_y_coord = previous_event['coordinates']['y']
                except:
                    pass
                
                try:
                    # distance
                    distance_from_last_event = sqrt((last_y_coord - y_coord)**2 + (last_x_coord - x_coord)**2)
                   
                    # change in angle
                    if rebond:
                        if rinkSide_of_the_team_that_shot == 'left':
                            last_distance_from_net =  sqrt((90 - last_x_coord)**2 + (last_y_coord-0)**2)
                            last_angle  = np.arcsin(last_y_coord/last_distance_from_net)
                        else:
                            last_distance_from_net =  sqrt((-90 - last_x_coord)**2 + (last_y_coord-0)**2)
                            last_angle  = -np.arcsin(last_y_coord/last_distance_from_net)

                        
                        change_in_angle = angle - last_angle
                    else:
                        change_in_angle = 0
                    
                    # speed
                    speed = distance_from_last_event / time_since_last_event        
                except:
                    pass
                
            
            all_data = [event_Idx, period, periodTime, id_team_that_shot,name_team_that_shot,result_event,x_coord,y_coord,distance_from_net,angle,rinkSide_of_the_team_that_shot,shot_type,empty_net,strength,last_event_type,last_x_coord,last_y_coord,distance_from_last_event,time_since_last_event,rebond,change_in_angle,speed,powerPlay,current_team_nb,other_team_nb]
            match_events_list.append(all_data+[type_season]+match_data)
            previous_event = item
    return match_events_list

def get_game_events(file_name_path,type_season)->pd.DataFrame:

    with open(file_name_path,'r') as f:
        data = json.loads(f.read())
        
        if 'messageNumber' in data and data['messageNumber'] == 2:
            return 'error'
        isLive =  data['gameData']['status']['abstractGameState']=='Live'
        all_list_data = get_file_event_rows_data(data,type_season)


    columns_name = [
    "event_Idx","period", "periodTime","id_team_that_shot","name_team_that_shot","result_event","x_coord","y_coord","distance","angle","rinkSide_of_the_team_that_shot",\
            "shot_type","empty_net","strength","last_event_type","last_x_coord","last_y_coord","distance_from_last","seconds_since_last","rebound","angle_change","speed",'powerplay','team_that_shot_nb','other_team_nb',\
            "type_season","id_game","season","team_away_name","team_home_name"]
    df = pd.DataFrame(all_list_data, columns=columns_name)
    return df,isLive