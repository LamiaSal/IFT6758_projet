# Importer comet_ml en haut de votre fichier, avant sklearn !
from comet_ml import Experiment
import os 

# Créer une expérience avec votre clé api
exp = Experiment(
    api_key=os.environ.get('COMET_API_KEY'),#ne pas coder en dur!
    project_name='milestone_2',
    #workspace=<YOUR_WORKSPACE>,
)
# ... Faire de la science des données ...
exp.log_metrics({"auc": auc, "acc": acc, "loss": loss})