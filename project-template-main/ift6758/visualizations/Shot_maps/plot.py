'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from scipy.ndimage import gaussian_filter
import numpy as np
class advance_plot():
    def __init__(self,csv_path:str,sigma=5):
        self.df = pd.read_csv(csv_path)
        self.sigma = sigma
        
    def get_figure(self):

        fig = go.Figure()
        fig.add_layout_image(
            dict
            (
                source=Image.open("../figures/nhl_rink.png"),
                xref="x",
                yref="y",
                x=-50,
                y=0,
                sizex=200,
                sizey=100,
                sizing="stretch",
                opacity=0.3,
                layer="above"
            )
        )

        team_names = self.df.columns[2:]
        for i, team in enumerate(team_names):

            if i == 0:
                contour = self.get_contour(team, visible=True)
            else:
                contour = self.get_contour(team)

            fig.add_trace(contour)

        buttons = []
        b_identity = np.identity(len(team_names),dtype=bool).tolist()
       
        for i,team_name in enumerate(team_names):
            buttons.append(dict(method='update',
                                label=team_name,
                                args=[{'visible': b_identity[i]}]
                                )
                        )
        updatemenu = [dict(
                        buttons=buttons,
                        x = 0.18,
                        y = 1.15,
        )]
       
        fig.update_layout( updatemenus=updatemenu)
       

        fig.update_layout( 
            title=dict
            (
                text= "2016-2017",
                font={'size':18}, 
                x= 0.5,
                     
            ),
           
            template="plotly_white"
        )

        return fig

    def get_contour(self,team_name:str,visible:bool = False):
    
        team_data = self.df[['x_coord','y_coord',team_name]]
        
        
        z = np.zeros((200,100))
        for index,row in team_data.iterrows():
            z[int(row['x_coord'])+100,int(row['y_coord'])+50] += row[team_name]

        z_smooth = gaussian_filter(z.T,self.sigma)       

        x = np.array(range(-100,100))
        y = np.array(range(-50,50))

        m = max(np.max(z_smooth), np.abs(np.min(z_smooth)))
        contour =  go.Contour(
                x = y,
                y = x, 
                z= z_smooth,
                colorscale='RdBu',
                zmax = m,
                zmin = -m,
                reversescale=True,
                connectgaps= False, 
                name = team_name,
                visible = visible
            )
        return contour
       
