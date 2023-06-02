import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools

def statistical_summary(dataframe: pd.DataFrame):
    """ 
    This function provides a general statistical summary
    
    args: 
        dataframe (pd.DataFrame): target Dataframe
    
    output: 
        dataframe (pd.DataFrame): Dataframe descriptive statistics
    
    Example usage: 
        statistical_summary(dataframe = dataframe)
    """
    # Splitting numerical from categorical data
    num_attributes = dataframe.select_dtypes( include=['int64', 'float64','int32', 'float32'] )
    
    # Central Tendency - Mean, Median
    ct1 = pd.DataFrame( num_attributes.apply( np.mean ) ).T
    ct2 = pd.DataFrame( num_attributes.apply( np.median ) ).T
    
    # dispersion - std, min, max, range, skew, kurtosis
    d1 = pd.DataFrame( num_attributes.apply( np.std ) ).T 
    d2 = pd.DataFrame( num_attributes.apply( min ) ).T 
    d3 = pd.DataFrame( num_attributes.apply( max ) ).T 
    d4 = pd.DataFrame( num_attributes.apply( lambda x: x.max() - x.min() ) ).T 
    d5 = pd.DataFrame( num_attributes.apply( lambda x: x.skew() ) ).T 
    d6 = pd.DataFrame( num_attributes.apply( lambda x: x.kurtosis() ) ).T 
    
    # coefficient of variation
    cv1 = d1/ct1
    
    # Putting all together
    m = pd.concat( [d2, d3, d4, ct1, ct2, d1, d5, d6,cv1] ).T.reset_index()
    m.columns = ['attributes', 'min', 'max', 'range', 'mean', 'median', 'std', 'skew', 'kurtosis', 'var_coef']
    return m; 

def correlation_matrix(dataframe:pd.DataFrame):
    """
    This function computes and plots a correlation matrix for all numerical columns
    
    Args: 
        dataframe (pd.DataFrame): Dataframe containing data of interest. 
    
    Returns: 
        heatmap based on correlation matrix
    
    Example usage: 
        correlation_matrix(dataframe = dataframe)
        
    """
    # Selection numerical columns
    num_cols = dataframe.select_dtypes( include=['int64', 'float64','int32', 'float32'] ).columns
    
    # Create correlation matrix
    corr_matrix = dataframe[num_cols].corr()

    # Create a mask to hide upper triangle of the plot
    mask = np.zeros_like(corr_matrix, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr_matrix, mask=mask, cmap=cmap, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt='.2f', annot_kws={"size": 10})
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.title('Correlation Matrix', fontsize=14)
    
    return plt.show();



def plot_categorical_features(dataframe: pd.DataFrame, 
                              ncols: int = 3, 
                              figsize: tuple = (15, 5), 
                              plot_type: str ='countplot', 
                              **kwargs):
    """
    Plots bar plots of categorical columns of a dataframe.

    Args
        dataframe (pd.DataFrame): dataframe of interest
    ncols (int): number of columns in the plot grid (default = 3)
    figsize (tuple): size of the figure (default = (15, 5)) 
    plot_type (str): Type of plot to use (default = 'countplot')
    **kwargs: Keyword arguments to be passed to the seaborn countplot/barplot function.

    Returns:
        None
    
    Example usage: 
        plot_categorical_features(dataframe = dataframe, 
                                    ncols = 3, 
                                    figsize = (15, 5), 
                                    plot_type = 'countplot')
    """
    # Keeping only categorical values
    cat_attributes = dataframe.select_dtypes( exclude = ['int64', 'float64','int32', 'float32','datetime64[ns]'])
    
    # setting number of rows
    if cat_attributes.shape[1] <= ncols: 
        nrows = 1
    else: 
        nrows = int(np.floor(cat_attributes.shape[1]/ncols))+1
    
    # Plotting data
    fig, axes = plt.subplots(nrows = nrows, ncols = ncols, figsize = figsize)
    for i, col in enumerate(cat_attributes):
        ax = axes.flat[i]
        if plot_type == 'countplot':
            sns.countplot(x = col, data = dataframe, ax = ax, **kwargs)
        elif plot_type == 'barplot':
            sns.barplot(x = col, y = 'count', 
                        data = dataframe.groupby(col).size().reset_index(name = 'count'), 
                        ax = ax, **kwargs)
        ax.set_title(col)
    
    # Returning figure 
    plt.tight_layout()
    return plt.show(); 

def plot_categorical_heatmap(dataframe:pd.DataFrame, 
                             figsize:tuple =(10, 8)):
    """
    Plots a heatmap of the counts of different categories for each pair of categorical variables in the input data frame.

    Args:
        data (pd.DataFrame): input data frame containing the categorical variables to plot
        figsize (tuple): figure size to use for the plot. (default = (10, 8))
    
    Returns:
        None
    
    Example usage: 
        plot_categorical_heatmap(dataframe = dataframe, 
                                figsize=(10, 8))

    """
    
    # Keeping only categorical variables
    cat_attributes = dataframe.select_dtypes( exclude=['int64', 'float64','int32', 'float32','datetime64[ns]'])
    cols = cat_attributes.columns
    
    # Empy data frame to be filled
    counts = pd.DataFrame(0, index=cols, columns=cols)
    
    # Compute the counts for each pair of categorical variables
    for i, col1 in enumerate(cols):
        for j, col2 in enumerate(cols):
            if i == j:
                counts.at[col1, col2] = dataframe[col1].count()
            else:
                counts.at[col1, col2] = dataframe.groupby([col1, col2]).size().shape[0]
    # Plot the heatmap
    plt.figure(figsize=figsize)
    ax = sns.heatmap(counts, 
                     annot=True, 
                     cmap='Blues')
    ax.set_title('Categorical Variables Heatmap')
    return plt.show();

def plot_clustered_bars(dataframe: pd.DataFrame, 
                        figsize: tuple = (20, 20)):
    """
    Creates a clustered bar chart for each combination of categorical variables in a pandas dataframe.
    
    Args:
        dataframe (pd.DataFrame): Input dataframe with categorical variables
        figsize (tuple): figure size to use for the plot. (default = (20,20))
    
    Returns:
        None
        
    Example usage 
        plot_clustered_bars(dataframe = dataframe)
    """
    # Get categorical variables
    cat_vars = dataframe.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not cat_vars:
        print("[Info] No categorical variables in input dataframe")
        return None 
    
    # Creating fig and axes
    num_vars = len(cat_vars)
    fig, axes = plt.subplots(nrows = num_vars, 
                             ncols = num_vars, 
                             figsize = figsize)
    
    # Going through possible interactions
    for i, var1 in enumerate(cat_vars):
        for j, var2 in enumerate(cat_vars):
            # Create a bar plot for the combination of variables
            if var1 == var2:
                sns.countplot(x = var1, 
                              data = dataframe, 
                              ax = axes[i,j])
                axes[i,j].set_xlabel('')
                axes[i,j].set_title(f"{var1}")
            else:
                sns.countplot(x = var1, 
                              hue = var2, 
                              data = dataframe, 
                              ax = axes[i,j])
                axes[i,j].legend_.remove()
                axes[i,j].set_title(f"{var1} vs {var2}")
    
    # Adjust spacing and layout
    plt.subplots_adjust(wspace=0.4, 
                        hspace=0.4)
    return plt.show(); 

def plot_categorical_numerical_interactions(dataframe:pd.DataFrame, 
                                            plot_type:str = 'violin'):
    """
    Plots the interaction between categorical variables and numerical variables in a dataframe.
    
    Args:
        dataframe (pd.DataFrame): input dataframe containing categorical and numerical variables.
        plot_type (str): type of figure to be used (boxplot, violin. Default = violin)
    
    Returns:
        None
    
    Example usage: 
        plot_categorical_numerical_interactions(dataframe = dataframe, 
                                                plot_type = 'violin')
    """
    
    # Get categorical and numerical variables
    cat_vars = dataframe.select_dtypes(include=['object', 'category']).columns.tolist()
    num_vars = dataframe.select_dtypes(include=['int', 'float']).columns.tolist()

    # Create figure
    nrows = len(num_vars)
    ncols = 3
    fig, axes = plt.subplots(nrows=nrows, 
                             ncols=ncols, 
                             figsize=(15, 5*nrows))

    # Loop through numerical variables
    for i, num_var in enumerate(num_vars):
        row_axes = axes[i]

        # Loop through categorical variables
        for j, cat_var in enumerate(cat_vars):
            # Plot categorical variable against numerical variable
            if plot_type == 'violin':
                sns.violinplot(x = cat_var, 
                               y = num_var, 
                               data = dataframe, 
                               ax = row_axes[j])
            if plot_type == 'boxplot':
                sns.boxplot(x = cat_var, 
                            y = num_var, 
                            data = dataframe, 
                            ax = row_axes[j])
            row_axes[j].set_title(f"{cat_var} vs {num_var}")
    # Adjust layout
    plt.tight_layout()
    return plt.show();


def scatterplot_matrix_numeric(dataframe:pd.DataFrame, 
                               more_than_two_values: bool = True):
    """Creates a scatterplot matrix for all pairs of numerical variables in the input dataframe.
    
    Arg: 
        dataframe (pd.DataFrame): input data frame
        more_than_two_values (bool): flag to keep variables with more than two values (default = True)

    Returns:
        None 
        
    Example usage: 
        scatterplot_matrix_numeric(dataframe = dataframe)
    """
    
    # Get numerical variables
    num_vars = dataframe.select_dtypes(include = ['int64', 'float64','int32', 'float32']).columns.tolist()
    
    # Making sure there are numerical variables
    if not num_vars:
        print("No numerical variables in input dataframe")
        return None; 

    # Create scatterplot matrix
    sns.set(style='ticks')
    if more_than_two_values: 
        num_var_2 = [var for var in num_vars if len(list(dataframe[var].unique())) > 2]
        sns.pairplot(dataframe[num_var_2], 
                     diag_kind ='kde')
    else: 
        sns.pairplot(dataframe[num_vars], 
                    diag_kind ='kde')
    
    # Rotate x-axis and y-axis tick labels
    plt.xticks(rotation = 45)
    plt.yticks(rotation = 45)
    
    return plt.show(); 
