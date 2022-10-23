'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np


class data_preprocessing_for_advanced_plot():
    def __init__(self,path_tidy,path_out,shape_arena=(200,85),side_to_rotate='left'):
        
        self.df = pd.read_csv(path_tidy)
        self.shape_arena = shape_arena
        self.side_to_rotate = side_to_rotate

        self.path_out = path_out
        pd.set_option('mode.chained_assignment', None)
    def get_all_seasons_stat(self,seasons):
        
        for season in seasons:
            self.get_season_stat(season)
        
    def get_season_stat(self,season):
        df_season = self.df[self.df['season']==season]
        df_season = self.pivot_season(df_season)
        avg = self.get_average_for_season(df_season)
        self.get_average_per_team_for_season(df_season,season,avg)
        
    def pivot_season(self,df_season):
        def pivot(x):
            return -x
        
        if self.side_to_rotate == 'left':
            df_season.loc[(df_season['rinkSide_of_the_team_that_shot'].isna()) & (df_season['x_coord'] > 0),'rinkSide_of_the_team_that_shot'] = self.side_to_rotate
        else:
            df_season.loc[(df_season['rinkSide_of_the_team_that_shot'].isna()) & (df_season['x_coord'] < 0),'rinkSide_of_the_team_that_shot'] = self.side_to_rotate 

        df_season.loc[df_season['rinkSide_of_the_team_that_shot']==self.side_to_rotate,'x_coord'] = df_season[df_season['rinkSide_of_the_team_that_shot']==self.side_to_rotate]['x_coord'].apply(pivot)
        df_season.loc[df_season['rinkSide_of_the_team_that_shot']==self.side_to_rotate,'y_coord'] = df_season[df_season['rinkSide_of_the_team_that_shot']==self.side_to_rotate]['y_coord'].apply(pivot)
        
        return df_season
    def binning(self,df):
        bin  = np.zeros(self.shape_arena)
        for row in df.iterrows():
            i = int(row[1]['x_coord'])+self.shape_arena[0]//2
            j = int(row[1]['y_coord'])+self.shape_arena[1]//2
            if i is None or j is None:
                continue
            bin[i,j] += int(row[1]['count'])
        return bin
        
    def get_average_for_season(self,df_season):
        avg_bins = np.zeros(self.shape_arena)
        # average shot per hour per emplacement
        df_question_2 = df_season.groupby(['x_coord','y_coord'])['x_coord'].count().reset_index(name="count").copy()
        avg_bins = self.binning(df_question_2)
        avg_bins/=2 *df_season["id_game"].nunique()  
        return avg_bins
    def get_average_per_team_for_season(self,df_season,season,avg_bins):
        df_question_3 = df_season.groupby(['x_coord','y_coord','name_team_that_shot'])['name_team_that_shot'].count().reset_index(name="count").copy()
        df_count_game_per_team = df_season.groupby(['name_team_that_shot'])["id_game"].nunique().reset_index(name="count_game_per_team").copy()
        d = dict()
        for team in df_season['team_home_name'].unique():
            bins = self.binning(df_question_3[df_question_3['name_team_that_shot']==team])
            bins/=  float(df_count_game_per_team[df_count_game_per_team['name_team_that_shot']==team]['count_game_per_team'].values[0])
            d[team] = (bins-avg_bins).tolist()  
        
        test=pd.DataFrame(d)
        test.to_pickle(f'{self.path_out}{season}.pkl')






