'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

class advance_plot():
    def __init__(self,csv_path:str,img_path,season,sigma=3):
        self.df = pd.read_csv(csv_path)
        self.sigma = sigma
        self.img_path = img_path
        self.season = season
        
    def get_figure(self):

        fig = go.Figure()
        fig.add_layout_image(
            dict
            (
                source=Image.open(self.img_path),
                xref="x",
                yref="y",
                x=-100,
                y=50,
                sizex=200,
                sizey=100,
                sizing="stretch",
                opacity=0.3,
                layer="above",
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
                text= f"season {self.season}",
                font={'size':18}, 
                x= 0.5,
            ),
           
            template="plotly_white"
        )


        #fig.data[0].colorbar.title = {"text":"Excess shots<br>per hour<br>(in %)"}
        fig.update_xaxes(
            constrain="domain",
        )
        fig.update_yaxes(
                    scaleanchor="x",
                    scaleratio = 0.85
                    )
        

        return fig

    def get_contour(self,team_name:str,visible:bool = False):
    
        team_data = self.df[['x_coord','y_coord',team_name]]
        
        
        z = np.ones((201,101))
        for index,row in team_data.iterrows():
            z[int(row['x_coord'])+100,int(row['y_coord'])+50] = int(row[team_name])

        z_smooth = gaussian_filter(z.T,self.sigma)       

        x = np.array(range(-100,101))
        y = np.array(range(-50,51))

        z_smooth = np.around(z_smooth,1)

        #print("yo",z_smooth)

        m = max(np.max(z_smooth), np.abs(np.min(z_smooth)))
        
        colorscale =['rgb(103,0,31)', #0
        'rgb(178,24,43)', #0.2
        'rgb(214,96,77)', #0.4
        'rgb(244,165,130)',#0.6
        'rgb(253,219,199)', # 0.8
        'rgb(250,250,250)', #0.8
        'rgb(250,250,250)',#1.0
        #'rgb(209,229,240)', # 1.2
        'rgb(146,197,222)', #1.4
        'rgb(67,147,195)', #1.6
        'rgb(33,102,172)', #1.8
        'rgb(5,48,97)']#2
        
        contour =  go.Contour(
                x = x,
                y = y,
                z= z_smooth,
                colorscale=colorscale, #px.colors.sequential.RdBu_r,#'RdBu',
                zmin=0,
                zmax=2,
                zmid=1,
                line_smoothing=1,
                reversescale=True,
                connectgaps= False,
                name = team_name,
                visible = visible,
                colorbar=dict(
                    title="Excess shots<br>per hour<br>(in ratio)", # title here
                    titleside='right',
                    titlefont=dict(
                        size=14,
                        family='Arial, sans-serif')
                )
            )
        
        return contour