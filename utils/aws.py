import pandas as pd
import boto3
from sqlalchemy import create_engine, text
from datetime import datetime
import utils
from pathlib import Path
import joblib
from InsuranceClass.HealthInsuranceClass import HealthInsurance

def getting_data_from_AWS_RDS(query: str, 
                              host: str, 
                              port:int, 
                              database: str, 
                              user: str, 
                              password: str): 
    """Downloads dataframe based on query pulling data from AWS RDS instance. 

    Args:
        query (str): SQL query to retrieve data 
        host (str): AWS host string
        port (str): AWS port 
        database (str): AWS database name
        user (str): AWS user
        password (str): AWS password
    
    Returns:
        pd.DataFrame with the ouput of query
    
    Example usage:
        getting_data_from_AWS_RDS(query = "SELECT * FROM TABLE" (with triple "s)
                                  host = 'XXX.XXX.XXX.rds.amazonaws.com', 
                                  port = 5432, 
                                  database = 'postgres', 
                                  user = 'super_safe_user', 
                                  password = 'super_safe_pass'):
    """
    # Creating connection
    conn_db = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    # Running query and importing it 
    with conn_db.begin() as conn:
        df = pd.read_sql(sql = text(query), 
                         con = conn)
        
    print(f'[Info] Data Frame with {df.shape[0]} rows and {df.shape[1]} columns imported successfully.')

    return df;

def update_data_to_AWS_S3(df: pd.DataFrame,
                          key: str,
                          aws_access_key_id: str , 
                          aws_secret_access_key: str,
                          bucket: str):
    """
    Uploads a Pandas DataFrame to an AWS S3 bucket.

    Args:
        df (pd.DataFrame): DataFrame to be uploaded
        bucket (str): Name of the S3 bucket to upload to
        key (str): Name to give to the uploaded file
        aws_access_key_id (str): AWS access key ID 
        aws_secret_access_key (str): AWS secret access key

    Returns:
        None

    Example usage: 
        update_data_to_AWS_S3(  df = df,
                                key = key,
                                aws_access_key_id = aws_access_key_id, 
                                aws_secret_access_key = aws_secret_access_key,
                                bucket = bucket)
    """
    # Creating time stamp
    today = datetime.today()#.strftime('%Y-%m-%d')
    
    # Convert the DataFrame to a CSV buffer
    csv_buffer = df.to_csv(index=False).encode('utf-8')

    # Create an S3 resource with the provided credentials
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    
    # Upload the CSV buffer to S3
    s3_path = f'data_versions/{today.year}/{today.month}/{today.day}/{key}.csv'
    s3.Object(bucket, s3_path).put(Body=csv_buffer)

    # Print a success message
    print(f'Uploaded {df.shape[0]} rows and {df.shape[1]} columns to s3://{bucket}/data_versions/{today.year}/{today.month}/{today.day}/{key}.csv')

    return None;




def upload_class_data_AWS_S3(df: pd.DataFrame, 
                             model_name: str,
                             bucket: str, 
                             aws_access_key_id: str , 
                             aws_secret_access_key: str,
                             testing_class: HealthInsurance,
                             aws_update: bool = False):
  
    """
    This function tests the HealthInsurance class while updating data versions to AWS S3 instance
    
    args: 
    df (pd.DataFrame): Dataframe with raw but clean data
    model_name (str): Model to be used when creating predictions
    bucket (str): bucket name to upload data
    testing_class (HealthInsurance): instance of the class of interest 
    aws_access_key_id (str): AWS access key ID 
    aws_secret_access_key (str): AWS secret access key
    aws_update (bool): A flag to allow data to be upload to S3 instance (False by default)

    
    output: 
    df (pd.DataFrame): Transformed data frame
    
    Example usage: 
        Upload_class_data_AWS_S3(df = df, 
                                model_name = model_name,
                                bucket = bucket, 
                                testing_class = testing_class,
                                aws_access_key_id = aws_access_key_id, 
                                aws_secret_access_key = aws_secret_access_key,
                                AWS_update = True)
    
    """
    # Dropping response column (present in training data)
    if 'response' in df.columns: 
        df = df.drop('response', axis = 1)
    
    if aws_update: 
        utils.update_data_to_AWS_S3(df = df,
                                    key = 'data_raw',
                                    aws_access_key_id = aws_access_key_id, 
                                    aws_secret_access_key = aws_secret_access_key,
                                    bucket = bucket)
        
    
    print(f'[Info] raw data created')
    # Creating copy for prediction method
    df_aux = df.copy()
    
    # Data cleaning and data upload
    df1 = testing_class.data_cleaning(df )
    
    if aws_update: 
        utils.update_data_to_AWS_S3(df = df1,
                                    key = 'data_cleaning',
                                    aws_access_key_id = aws_access_key_id, 
                                    aws_secret_access_key = aws_secret_access_key,
                                    bucket = bucket)
    print(f'[Info] data_cleaning method applied')

    # Feature engineering and data upload
    df2 = testing_class.feature_engineering(df1)
    
    if aws_update: 
        utils.update_data_to_AWS_S3(df = df2,
                                    key = 'feature_engineering',
                                    aws_access_key_id = aws_access_key_id, 
                                    aws_secret_access_key = aws_secret_access_key,
                                    bucket = bucket)
    print(f'[Info] feature_enginerring method applied')

    # Data preparation and data upload
    df3 = testing_class.data_preparation(df2)
    
    if aws_update: 
        utils.update_data_to_AWS_S3(df = df3,
                                    key = 'data_preparation',
                                    aws_access_key_id = aws_access_key_id, 
                                    aws_secret_access_key = aws_secret_access_key,
                                    bucket = bucket)
    print(f'[Info] data_preparation method applied')

    # Selection model 
    model_name_aux = model_name+'.pkl'
    model_path = Path.cwd() /'models'/'models'/ model_name_aux
    model = joblib.load(model_path)

    # Data prediction and data upload
    df4 = testing_class.prediction(model, df3, df_aux)
    if aws_update: 
        utils.update_data_to_AWS_S3(df = df4,
                                    key = 'prediction_'+model_name,
                                    aws_access_key_id = aws_access_key_id, 
                                    aws_secret_access_key = aws_secret_access_key,
                                    bucket = bucket)

    print(f'[Info] prediction method applied')

    return df4