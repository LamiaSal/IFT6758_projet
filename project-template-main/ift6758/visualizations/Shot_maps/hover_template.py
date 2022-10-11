'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon : neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # Define and return the hover template
    hovertemp= '        <b style="font-family:Roboto Slab">Neighborhood: </b><span style="font-family:Roboto"> %{y}</span><br>'
    hovertemp+='        <b style="font-family:Roboto Slab">Year: </b><span style="font-family:Roboto"> %{x}</span> <br>'
    hovertemp+='        <b style="font-family:Roboto Slab">Trees Planted: </b><span style="font-family:Roboto"> %{z} </span><br>'
    hovertemp+='<extra></extra>'
    return hovertemp
