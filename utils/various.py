from dotenv import load_dotenv
import os 

def load_credentials():
    """
    This function load credentials from .env file

    Args: 
        None
    
    Returns:
        sets of credentials

    Example usage:
        rds_credentials, s3_credentials = load_credentials()
        
    """
    load_dotenv()
    rds_credentials = {'user': os.getenv('user'),
                        'host': os.getenv('host'),
                        'port': os.getenv('port'),
                        'database': os.getenv('database'),
                        'password': os.getenv('password')}
    s3_credentials = {'aws_access_key_id':  os.getenv('AWS_ACCESS_KEY_ID'), 
                      'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')}
    return rds_credentials, s3_credentials;