'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import pandas as pd
import hover_template
import preprocess
import plotly.graph_objects as go
import hover_template
from PIL import Image

def get_figure():
    '''
        Generates offensive shot map 1.

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''

    # Create the heatmap with dragmode=False in the layout. And, hover template included
    pyLogo = Image.open("../../../figures/nhl_rink.png").convert("RGB")
    fig = px.imshow(pyLogo, zmin=50, zmax=200)

    fig.update_layout(yaxis_title="", # TODO
                    xaxis_title="") # TODO


    # Set templates
    fig.update_layout(template="plotly_white")
    fig.show()

    '''
    fig = px.imshow(data,labels=dict(color="Trees"),x=data.keys(), y=data.index, color_continuous_scale=px.colors.sequential.Bluyl)
    fig = fig.update_layout(dragmode=False)
    
    fig = fig.update_traces(
        hovertemplate = hover_template.get_heatmap_hover_template()
    )
    '''
    return fig
