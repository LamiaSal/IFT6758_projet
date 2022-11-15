
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.calibration import CalibrationDisplay

sns.set_theme()

def log_ROC(y_true,y_preds,experiment):
    fpr, tpr, _ = metrics.roc_curve(y_true, y_preds)
    roc_auc = metrics.auc(fpr, tpr)
    fig = plt.figure()
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    experiment.log_figure(figure=fig)
    experiment.log_metrics({'AUC':roc_auc})

def log_Calibration(y_true,y_probs,experiment):
    disp = CalibrationDisplay.from_predictions(y_true, y_probs)
    disp.ax_.set_title('Calibration curve')
    experiment.log_figure(figure=disp)

def log_GoalRate(y_probs,experiment):
    
    centiles = range(0,99,5)

    value = np.percentile(y_probs,range(0,100,5))   
    fig = plt.figure()
    plt.title('Goal Rate')
    plt.ylabel('Goals / (Shots + Goals)')
    plt.xlabel('Shot probability model percentile')

    plt.plot(np.array(centiles)/100.0,value,label='model 1')
    plt.legend()
    plt.gca().invert_xaxis()

    ys = range(0,101,10)
    yticks= [str(y)+'%' for y in ys]
    plt.yticks(np.array(ys)/100,yticks)
    plt.xticks(np.array(ys)/100,ys)
    experiment.log_figure(figure=fig) 
    
def log_Cumulative(y_probs,experiment):
    centiles = range(0,101,5)
    value = np.percentile(y_probs,centiles)

    cumulative_sum = np.cumsum(value[::-1])/np.sum(value)
    fig = plt.figure()
    plt.title('Cumulative % of goals')
    plt.ylabel('Proportion')
    plt.xlabel('Shot probability model percentile')

    plt.plot(np.array(centiles)/100,cumulative_sum[::-1],label='model 1')
    plt.legend()
    plt.gca().invert_xaxis()

    ys = range(0,101,10)
    yticks= [str(y)+'%' for y in ys]
    plt.yticks(np.array(ys)/100,yticks)
    plt.xticks(np.array(ys)/100,ys)
    experiment.log_figure(figure=fig)  

def log_metrics(y_true,y_preds,experiment):
    acc = metrics.accuracy_score(y_true,y_preds)
    recall = metrics.recall_score(y_true,y_preds,average='macro')
    precision = metrics.precision_score(y_true,y_preds,average='macro')
    f_score = metrics.f1_score(y_true,y_preds,average='macro')

    experiment.log_metrics({
        'Accuracy':acc,
        'Recall':recall,
        'Precision':precision,
        'f_score':f_score
        })
    matrix = metrics.confusion_matrix(y_true,y_preds)
    experiment.log_confusion_matrix(labels=["Missed", "Goal"],matrix=matrix)

def log_All(y_true,y_preds,y_probs,experiment):
    log_metrics(y_true,y_preds,experiment)
    log_ROC(y_true,y_preds,experiment)
    log_Calibration(y_true,y_probs,experiment)
    log_GoalRate(y_probs,experiment)
    log_Cumulative(y_probs,experiment)