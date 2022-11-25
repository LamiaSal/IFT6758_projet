# IFT6758 Repo Project

In the repository you'll find the work we've done through the whole project of the MILA course IFT6758. This project was divided in 3 parts.
# Milestone 2
In this ***second part*** we had to create a Comet account, do features engineering, train models and evaluate our performance on a test set.

## Comet
Just the link to our [Comet](https://www.comet.com/princesslove/itf-6758-team-4/view/new/panels).

## Features engineering
The features engineering was done in two jupyter notebooks [Features engineering for Q2](./notebooks/Part_2_Q.2.ipynb) and [Features engineering for Q4](./notebooks/Part-2_Q.4-Tidy.ipynb).

An example of the features engineering can be found on Comet: [example](https://www.comet.com/princesslove/itf-6758-team-4/2289a0e68c43462eafc910ef9f356de7?assetId=9d8cd18edbe747748e16edfdaa47d4b8&assetPath=dataframes&experiment-tab=assets). The code that generated this example can be found [here](./ift6758/tidying_data/milestone2_tidying_data.py).

The actual dataset with the features engineered can be found on a google drive [here](https://drive.google.com/file/d/1kM__riNHRPx5GsyuOH3yhiql3OZvwmuP/view?usp=share_link).

## Training models
The actual training of the different models can be found in 3 differents notebooks: [Logistic Regression Q3](./notebooks/Part_2_Q.3.ipynb), [XGBoost Q5](./notebooks/Part_2_Q.5.ipynb) and [Neural Nets Q6](./notebooks/Part_2-Q6.ipynb)

Functions to preprocess the data and to send information to Comet such as Metrics, plots and models can be found in the [utils file](./ift6758/models/utils.py). 

Functions to plot all the 4 graphs (ROC, Calibration, Goal percentile and Cumulative goal percentile) can be found [here](./ift6758/models/plotter.py).

## Evaluating models
The evaluation of the models and comparison of their performance has been done in a jupyter notebook: [Evaluation Q7](./notebooks/Part_2_Q.7.ipynb).

# Milestone 1

## Data wrangling and exploration
In the ***first part*** we had to extract, tidy and visualize data of the LNH statistics API (https://gitlab.com/dword4/nhlapi). In this repository you'll find :

- the directory [`./datasets`](./datasets) where the json files were downloaded and where we've put all the csv files created from the API data. On this github no files are uploaded. Nevertheless, "tidy_data.csv" file on a accessible google drive link (https://drive.google.com/file/d/1vuIGiBWieIcheFwg2HYMPN2R5I3KWEpX/view?usp=sharing). In this file we have all the necessary data to plot the visualizations.
- the directory "figures" where can be found a map of the NHL rink :

<p align="center">
<img src="./figures/nhl_rink.png" alt="NHL Rink is 200ft x 85ft." width="400"/>
<p>

The image can be found in [`./figures/nhl_rink.png`](./figures/nhl_rink.png).
    
In the directory [`./ift6758`](./ift6758), can be found all the the sources code in .py for the differents questions:
    
- The code to fetch the json files from the API can be found in [`./ift6758/data`](./ift6758/data)
- The code to tidy the json files can be found in [`./ift6758/tidy_data`](./ift6758/tidy_data). The jupyternotebook version can also be found in [`./notebooks/Q.4_tidying_data.ipynb`](./notebooks/Q.4_tidying_data.ipynb). This code provides a "tidy_data.csv" that is accesible from this link (https://drive.google.com/file/d/1vuIGiBWieIcheFwg2HYMPN2R5I3KWEpX/view?usp=sharing). All the following tasks (debogger, and visualizations code can be ran without downloading anything).
- In [`./ift6758/visualizations`](./ift6758/visualizations) there are several code that are used for the different visualizations. Especially, you may find the code for the advanced visualization (a preprocessing method [`./ift6758/visualizations/Q6_visualisations_avancées/preprocess.py`](./ift6758/visualizations/Q6_visualisations_avancées/preprocess.py) to extract excess shot rate per hour per season per team, and a method to plot the shot maps [`./ift6758/visualizations/Q6_visualisations_avancées/plot.py`](./ift6758/visualizations/Q6_visualisations_avancées/plot.py)).
    
In the directory [`./notebooks`](./notebooks), can be found all the the jupyternotebooks to answer the different questions. 
- The jupyternotebooks [`./notebooks/Q.2_Outil_de_débogage.ipynb`](./notebooks/Q.2_Outil_de_débogage.ipynb), [`./notebooks/Q.5_visualisations_simples.ipynb`](./notebooks/Q.5_visualisations_simples.ipynb) and [`./notebooks/Q.6_visualisations_avancées.ipynb`](./notebooks/Q.6_visualisations_avancées.ipynb) can be ran without prior requirements (without downloading anything). 
- To run the jupyternotebook  [`./notebooks/Q.4_tidying_data.ipynb`](./notebooks/Q.4_tidying_data.ipynb) you'll have to fetch the json files by running [`./ift6758/data/data_fetching.py`](./ift6758/data/data_fetching.py)


## Installation

To install this package, first setup your Python environment by following the instructions in the [Environment](#environments) section.
Once you've setup your environment, you can install this package by running the following command from the root directory of your repository. 

    pip install -e .

You should see something similar to the following output:

    > pip install -e .
    Obtaining file:///home/USER/project-template
    Installing collected packages: ift6758
    Running setup.py develop for ift6758
    Successfully installed ift6758-0.1.0


## Environments

The first thing you should setup is your isolated Python environment.
You can manage your environments through either Conda or pip.
Both ways are valid, just make sure you understand the method you choose for your system.
It's best if everyone on your team agrees on the same method, or you will have to maintain both environment files!
Instructions are provided for both methods.

**Note**: If you are having trouble rendering interactive plotly figures and you're using the pip + virtualenv method, try using Conda instead.

### Conda 

Conda uses the provided `environment.yml` file.
You can ignore `requirements.txt` if you choose this method.
Make sure you have [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/individual) installed on your system.
Once installed, open up your terminal (or Anaconda prompt if you're on Windows).
Install the environment from the specified environment file:

    conda env create --file environment.yml
    conda activate ift6758-conda-env

After you install, register the environment so jupyter can see it:

    python -m ipykernel install --user --name=ift6758-conda-env

You should now be able to launch jupyter and see your conda environment:

    jupyter-lab

If you make updates to your conda `environment.yml`, you can use the update command to update your existing environment rather than creating a new one:

    conda env update --file environment.yml    

You can create a new environment file using the `create` command:

    conda env export > environment.yml

### Pip + Virtualenv

An alternative to Conda is to use pip and virtualenv to manage your environments.
This may play less nicely with Windows, but works fine on Unix devices.
This method makes use of the `requirements.txt` file; you can disregard the `environment.yml` file if you choose this method.

Ensure you have installed the [virtualenv tool](https://virtualenv.pypa.io/en/latest/installation.html) on your system.
Once installed, create a new virtual environment:

    vitualenv ~/ift6758-venv
    source ~/ift6758-venv/bin/activate

Install the packages from a requirements.txt file:

    pip install -r requirements.txt

As before, register the environment so jupyter can see it:

    python -m ipykernel install --user --name=ift6758-venv

You should now be able to launch jupyter and see your conda environment:

    jupyter-lab

If you want to create a new `requirements.txt` file, you can use `pip freeze`:

    pip freeze > requirements.txt



