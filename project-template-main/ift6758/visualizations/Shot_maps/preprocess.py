'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np


def get_mean_of_shot_per_region(csv_path:str):

    data = pd.read_csv(csv_path)
    data_2016 = data[data['season']==20162017]
    print(data_2016.head())
    x = np.zeros(200)
    y = np.zeros(100)


    for index, row in data_2016.iterrows():
        print(row)



if __name__ == '__main__':
    get_mean_of_shot_per_region(r'datasets\tidy_data.csv')



