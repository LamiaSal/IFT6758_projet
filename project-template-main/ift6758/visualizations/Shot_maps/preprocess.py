'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np


def export_data_to_plot(season,path):
    
    def pivot(x):
        return -x

    df = pd.read_csv(path)
    df_season = df[df["season"]==season]
    
    side_to_rotate = 'left'
    if side_to_rotate == 'left':
        df_season.loc[(df_season['rinkSide_of_the_team_that_shot'].isna()) & (df_season['x_coord'] > 0),'rinkSide_of_the_team_that_shot'] = side_to_rotate 
    else:
        df_season.loc[(df_season['rinkSide_of_the_team_that_shot'].isna()) & (df_season['x_coord'] < 0),'rinkSide_of_the_team_that_shot'] = side_to_rotate 
        
    df_season.loc[df_season['rinkSide_of_the_team_that_shot']==side_to_rotate,'x_coord'] = df_season[df_season['rinkSide_of_the_team_that_shot']==side_to_rotate]['x_coord'].apply(pivot)
    df_season.loc[df_season['rinkSide_of_the_team_that_shot']==side_to_rotate,'y_coord'] = df_season[df_season['rinkSide_of_the_team_that_shot']==side_to_rotate]['y_coord'].apply(pivot)
    
   
    # average shot per hour per emplacement
    df_question_2 = df_season.groupby(['x_coord','y_coord'])['x_coord'].count().reset_index(name="count")
    df_question_2["mean_shots_per_hour_in_whole_league"] = df_question_2["count"]/df_season["id_game"].nunique() 

    # count per team per emplacement
    df_question_3 = df_season.groupby(['x_coord','y_coord','name_team_that_shot'])['name_team_that_shot'].count().reset_index(name="count_per_team")
    df_question_3_p = df_question_3.pivot(index=["x_coord","y_coord"], columns="name_team_that_shot", values="count_per_team")
  
    # count game per team
    df_count_game_per_team = df_season.groupby(['name_team_that_shot'])["id_game"].nunique().reset_index(name="count_game_per_team")
    
    # compute probability of number of shots per emplacemnt per hour per team
    for team in df_question_3_p.columns :
        df_question_3_p[team] /= df_count_game_per_team[df_count_game_per_team["name_team_that_shot"]==team]["count_game_per_team"].values
    
    print("begin 2 minutes task")
    # percentage
    for x,y in  df_question_3_p.index:
        alpha = df_question_2.query(f'x_coord == {x} and y_coord == {y}')["mean_shots_per_hour_in_whole_league"].values
        df_question_3_p[(df_question_3_p.index.get_level_values('x_coord')==x) & (df_question_3_p.index.get_level_values('y_coord')==y)]=\
            df_question_3_p[(df_question_3_p.index.get_level_values('x_coord')==x) & (df_question_3_p.index.get_level_values('y_coord')==y)].apply(lambda x: x//alpha)
    
    df_question_3_p[df_question_3_p.isna()]=int(1)
    
    df_question_3_p.to_csv(f"../datasets/data_to_plot_per_{season}.csv")

    return df_question_3_p


if __name__ == '__main__':
    
    path ='../datasets/tidy_data.csv'
    export_data_to_plot(20162017,path)



