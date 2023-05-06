# Insurance Cross-selling Ranking Model
This is an end-to-end project developed by [Your Name] to showcase a ranking model developed to assist decision making in a marketing campaign within an insurance company looking to increase the cross-selling rates. The model was developed using Python and XGBoost, and deployed through a FastAPI API hosted on AWS Lambda.

## Objective
The objective of this project is to develop a ranking model to predict the probability of purchase of new clients in a marketing campaign to cross-sell an insurance product to existing customers. The model is trained on historical data obtained from previous campaigns, and the output is a ranking score that ranks the customers by their probability of purchase.

## Data
The data used for this project was obtained from the insurance company's database and contains information about existing customers who were targeted in previous cross-selling campaigns. The dataset includes the following variables:

- Gender
- Age
- Driving License
- Region Code
- Previously Insured
- Vehicle Age
- Vehicle Damage
- Annual Premium
- Policy Sales Channel
- Vintage
- Response (target variable)

## Model
The model used in this project is an XGBoost model that was fine-tuned using a Bayesian optimization approach. The model was trained on the historical data obtained from previous campaigns, and the output is a ranking score that ranks the customers by their probability of purchase.

## API
The model was deployed through a FastAPI API that is hosted on AWS Lambda. The API accepts a JSON file containing the variables for each customer and returns a JSON file containing the ranking score for each customer. The API was tested using Pytest, and the tests are included in the repository.

<img src="models/figures/xgboost_finetuned.png" width="600" height="300" />


## Project Deployment

The general overview for the deployment of this project is presented as follows: 

<img src="project_architecture.png" width="600" height="400" />

## Demo

<img src="cross_sell_demo.gif" width="660" height="418" />


