
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.calibration import CalibrationDisplay

sns.set_theme()

def log_ROC(y_true,y_preds,model_names = None):
    fig = plt.figure()
    if isinstance(y_preds, list):
        for y_pred, model_name in zip(y_preds,model_names):
            fpr, tpr, _ = metrics.roc_curve(y_true, y_pred)
            roc_auc = metrics.auc(fpr, tpr)
            plt.title('Receiver Operating Characteristic')
            plt.plot(fpr, tpr, 'b', label = f'{model_name} AUC = %0.2f' % roc_auc)
    else : 
        fpr, tpr, _ = metrics.roc_curve(y_true, y_preds)
        roc_auc = metrics.auc(fpr, tpr)
        plt.title('Receiver Operating Characteristic')
        plt.plot(fpr, tpr, 'b', label = f'{model_names} AUC = %0.2f' % roc_auc)

    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    return fig, roc_auc
    

def log_Calibration(y_true,y_probs,model_names = None):
    fig = plt.figure()
    # Just a figure and one subplot
    fig, ax = plt.subplots()
    if isinstance(y_probs, list):
        for y_prob, model_name in zip(y_probs,model_names):
            disp = CalibrationDisplay.from_predictions(y_true, y_prob,name=model_name,ax=ax)
    else :
        disp = CalibrationDisplay.from_predictions(y_true, y_probs,name=model_names,ax=ax)
    disp.ax_.set_title('Calibration curve')
    return disp.figure_

def log_GoalRate(y_probs,model_names = None):
    fig = plt.figure()
    plt.title('Goal Rate')
    plt.ylabel('Goals / (Shots + Goals)')
    plt.xlabel('Shot probability model percentile')

    centiles = range(0,99,5)
    if isinstance(y_probs, list):
        for y_prob, model_name in zip(y_probs,model_names):
            value = np.percentile(y_prob,range(0,100,5))   
            plt.plot(np.array(centiles)/100.0,value,label=model_name)
    else: 
        value = np.percentile(y_probs,range(0,100,5))   
        plt.plot(np.array(centiles)/100.0,value,label=model_names)
    
    plt.legend()
    plt.gca().invert_xaxis()

    ys = range(0,101,10)
    yticks= [str(y)+'%' for y in ys]
    plt.yticks(np.array(ys)/100,yticks)
    plt.xticks(np.array(ys)/100,ys)

    return fig
    
    
def log_Cumulative(y_probs,model_names = None):
    centiles = range(0,101,5)
    
    
    fig = plt.figure()
    plt.title('Cumulative % of goals')
    plt.ylabel('Proportion')
    plt.xlabel('Shot probability model percentile')
    if isinstance(y_probs, list):
        for y_prob, model_name in zip(y_probs,model_names):
            value = np.percentile(y_prob,centiles)
            cumulative_sum = np.cumsum(value[::-1])/np.sum(value)
            plt.plot(np.array(centiles)/100,cumulative_sum[::-1],label=model_name)
    else : 
        value = np.percentile(y_probs,centiles)
        cumulative_sum = np.cumsum(value[::-1])/np.sum(value)
        plt.plot(np.array(centiles)/100,cumulative_sum[::-1],label=model_names)
    plt.legend()
    plt.gca().invert_xaxis()

    ys = range(0,101,10)
    yticks= [str(y)+'%' for y in ys]
    plt.yticks(np.array(ys)/100,yticks)
    plt.xticks(np.array(ys)/100,ys)
    return fig
      

def log_metrics(y_true,y_preds,model_names,experiment):
    acc = metrics.accuracy_score(y_true,y_preds)
    recall = metrics.recall_score(y_true,y_preds,average='macro')
    precision = metrics.precision_score(y_true,y_preds,average='macro')
    f_score = metrics.f1_score(y_true,y_preds,average='macro')
    
    # log confusion matrix
    matrix = metrics.confusion_matrix(y_true,y_preds,)
    experiment.log_confusion_matrix(labels=["Missed", "Goal"],matrix=matrix,title=f"Confusion Matrix {model_names}")

    experiment.log_metrics({
        'model_name':model_names,
        'Accuracy':acc,
        'Recall':recall,
        'Precision':precision,
        'f_score':f_score
        })
    

def log_All(y_true,y_preds,y_probs,model_names,experiment):
    log_metrics(y_true,y_preds,model_names,experiment)

    # log roc_auc
    fig_roc_auc, roc_auc  = log_ROC(y_true,y_preds,model_names)
    experiment.log_figure(figure=fig_roc_auc)
    experiment.log_metrics({'AUC':roc_auc})

    # log Calibration
    fig_calibration = log_Calibration(y_true,y_probs,model_names)
    experiment.log_figure(figure=fig_calibration)

    # log Goal Rate
    fig_goalRate = log_GoalRate(y_probs,model_names)
    experiment.log_figure(figure=fig_goalRate)

    # log Cumulative
    fig_cumulative = log_Cumulative(y_probs,model_names)
    experiment.log_figure(figure=fig_cumulative)