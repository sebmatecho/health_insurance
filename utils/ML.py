import pandas as pd
import matplotlib.pyplot as plt
import scikitplot as skplt
from sklearn import metrics
import os
import pickle
from pathlib import Path



def model_figures(y_target: pd.Series,
                  X_pred:pd.DataFrame,
                  y_pred: pd.Series, 
                  model_name: str, 
                  model): 
    """Creates Cumulative Gain and Lift curves figures (good for ranking metrics)
      
      Args:
          y_target (pd.Series): Target variable
          X_pred (pd.DataFrame): Target dataframe
          y_pred (pd.Series): predicted values
          model_name (str): Model Name
          model: model instance
      
      Returns:
          a 2x1 figure displaying matplotlib figures
      
      Example usage:
          model_figures(y_target = y_val,
                        X_pred = X_pred,           
                        y_pred = yhat_knn, 
                        model_name = 'K-nearest neighboors'
                        model = model)
          
    """
    # create a 1 row, 2 column subplot
    fig, ax = plt.subplots(1, 3, figsize=(21, 7))
    
    # plot the cumulative gain curve on the left
    skplt.metrics.plot_cumulative_gain(y_target, y_pred, ax=ax[0])
    
    # plot the lift curve on the right
    skplt.metrics.plot_lift_curve(y_target, y_pred, ax=ax[1])

    #plot ROC curve
    skplt.metrics.plot_roc_curve(y_target, y_pred, ax=ax[2])
    
    # set some titles and labels
    ax[0].set_title('Cumulative Gain Curve: '+model_name)
    ax[0].set_xlabel('Percentage of sample')
    ax[0].set_ylabel('Gain')
    ax[1].set_title('Lift Curve: '+model_name)
    ax[1].set_xlabel('Percentage of sample')
    ax[1].set_ylabel('Lift')
    ax[1].legend(loc='upper right')
    ax[2].set_title('ROC Curve: '+model_name)
    ax[2].set_xlabel('False Positive Rate (FPR)')
    ax[2].set_ylabel('True Positive Rate (TPR)')
    
    return fig;


def model_assessment(models: dict,
                     x_train: pd.DataFrame, 
                     y_train: pd.DataFrame,
                     x_test: pd.DataFrame, 
                     y_test: pd.DataFrame,
                     destination_figures: str = 'figures',
                     destination_models: str = 'models'):
    """ Fits and assesses ML models based on ranking metrics (Cumulative and Lift curves)
    Args:
          models (dict): Model name (key) and model instance (item, including hyper-parameters)
          x_train (pd.dataframe): training dataframe
          y_train (pd.dataframe): training target
          x_test (pd.dataframe): testing dataframe
          y_test (pd.dataframe): testing target
          destination_figures (str): folder name where figures are to be stored (set as 'figures' by default)
          destination_figures (str): folder name where models are to be stored (set as 'models' by default)
      
      Returns:
          Creates directory where cumulative and lift curves plots and serialized (pickle) models are stored
      
      Example usage:
          model_assessment( models = models,
                            x_train = x_train, 
                            y_train = y_train,
                            x_test = x_test
                            y_test = y_test,
                            destination_figures = 'figures',
                            destination_models = 'models')
    """
    # Creating directory to save figures
    models_main_path = Path.cwd().parent / 'models'
    
    root_path = os.path.join(models_main_path, destination_figures)
    figures_path = Path(root_path)
    if figures_path.exists():
        print(f'[Info] Path {figures_path} already exists.')
    else:
        figures_path.mkdir(parents= True, exist_ok = True)
        print(f'[Info] Path{figures_path} created.')
    
    # Creating directory to save trained models
    root_path = os.path.join(models_main_path,destination_models)
    models_path = Path(root_path)
    if models_path.exists():
        print(f'[Info] Path {models_path} already exists.')
    else:
        models_path.mkdir(parents= True, exist_ok = True)
    print(f'[Info] Path {models_path} created.')
    
    # train each model and export the cumulative gains curve and lift curve and models
    for i, (name, model) in enumerate(models.items()):
        # fit the model to the training data
        model.fit(x_train, y_train)
        
        # Setting model object name 
        file_name_model = name.lower().replace(' ','_')+'.pkl'
        
        # Exporting model
        with open(models_path/file_name_model, 'wb') as file: 
          pickle.dump(model, file)
        
        # make predictions on the test data
        y_proba = model.predict_proba(x_test)
        
        # Setting model object name 
        file_name = name.lower().replace(' ','_')+'.png'
        file_name_fig = figures_path/file_name
        
        # Exporting figure
        fig = model_figures(y_target= y_test,
                            X_pred = x_test,
                            y_pred= y_proba, 
                            model_name = name, 
                            model = model)
        
        fig.savefig(file_name_fig, dpi=300, bbox_inches='tight', pad_inches=0.2)
        print(f'[Info] {name} results exported successfully')
        
    return None;