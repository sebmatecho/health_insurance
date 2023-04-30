from typing import List 
from pathlib import Path
from mangum import Mangum
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from InsuranceClass.HealthInsuranceClass import HealthInsurance


import pandas as pd
import requests
import xgboost
import uvicorn
import json
import os
import joblib


# Load pre-trained model
home_path = Path.cwd()
model_path = home_path /'models'/'models'/ 'xgboost_finetuned.pkl'
model = joblib.load(model_path)


# Define the FastAPI app
app = FastAPI()

# Define the input data model
class InputData(BaseModel):
    gender: str
    age: int
    driving_license: int
    region_code: int
    previously_insured: int
    vehicle_age: str
    vehicle_damage: str
    annual_premium: int
    policy_sales_channel: int
    vintage: int    

# Define the output data model
class OutputData(BaseModel):
    gender: str
    age: int
    driving_license: int
    region_code: int
    previously_insured: int
    vehicle_age: str
    vehicle_damage: str
    annual_premium: int
    policy_sales_channel: int
    vintage: int
    prediction: float

# Define the API endpoint
# Set input and output classes for predict: Lists 
@app.post('/predict/', response_model=List[OutputData])
async def predict(input_data: List[InputData]):
    # Convert list of instances to list of dicts
    dict_list = [d.dict() for d in input_data]
    # Convert list of dicts to DataFrame
    input_data = pd.DataFrame(dict_list)
    # Create copy for final output
    df_final = input_data.copy()
    # Creatint pipeline 
    pipeline = HealthInsurance()
    # Data Cleaning
    df1_post = pipeline.data_cleaning(input_data)
    # Feature engineering
    df2_post = pipeline.feature_engineering(df1_post)
    # Data preparation
    df3_post = pipeline.data_preparation(df2_post)
    # Data prediction
    prediction = pipeline.prediction(model,df3_post,df_final)
    # Send response
    return JSONResponse(content = prediction.to_json() )

handler = Mangum(app, lifespan="off")