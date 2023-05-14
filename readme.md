# Insurance Cross-selling Ranking Model

## Abstract 

Whitin an insurance company, a marketing campaing aiming to increase cross-sell rates is going to be held. The featuring product for such campaing is vehicle insurance and is expected to target current life insurace policyholders. Data involving demographics (gender, age, region), Vehicles (Vehicle Age, Damage), Policy (Premium, sourcing channel) and of course, end result for this campaing; was collected during the initial iteration of it. The insurance company is interested in better targeting the potential clients based on what was learnt during such first iteration. Being able to prioritize clients would be of tremendous use to the managers as communication strategy can be adjusted accordingly leading to optimized business model and revenue.  

Under the following assumptions: 
- 1M clients are to be reached telephonically to be told about the product
- all clients are expected to be reached
- average of 12 calls per hour per agent
- average agent salary 20 USD/hour 


**The estimate cost of such campaing is about $1.6M USD**

This is an end-to-end data project aiming to propose a ranking model developed to assist decision making in such campaing. The project was entirely developed using Python. A bayesian fined tuned XGBoost model (predicting the probability of clients being interested in the product) was deployed through a FastAPI API hosted on Render is available to use in a google sheets spreadsheet. According to obtained results, this model should be able to rank (prioritize) clients in a way that reaching the top 20% of the database lead to 90% of the expected outcome of the entire campaign, and thus reducing campaing costs by 80%. 

**The estimate cost of such campaing using the proposed solution approach is about $330K USD**
## Demo

If the Google Apps Script API is enabled in your gmail account settings, you are more than welcome to try it out [here](https://docs.google.com/spreadsheets/d/1WUQPmwvzYX_OY9WIVluOEKeaUD4erhhSXdbbLip4ElY/edit?usp=sharing). Please, be mindful that the API was deployed on a free tier resources, so it might take a while (30-60 secs). 

You can propose your own selection of values for the variables, but if you need a starting point, there you go: 

```
Male	33	1	15	0	1-2 Year	Yes	28267	154	269
Female	69	1	28	0	1-2 Year	Yes	25126	124	98
Male	23	1	26	0	< 1 Year	Yes	46132	160	180
```

Once pasted, hit the *Sebmatecho* menu and select the *Get Prediction* option. You will get a predicted probability for such person to be interested into the producted being prometed. 

<img src="cross_sell_demo.gif" width="660" height="418" />

## Objective

The objective of this project is to develop a ranking model to predict the probability of purchase of new clients in a marketing campaign to cross-sell an insurance product to existing customers. The model is trained on historical data obtained from previous campaigns, and the output is a ranking score that ranks the customers by their probability of purchase.

## Data
The data used for this project was obtained from Kaggle (description and further details available [here](https://www.kaggle.com/datasets/anmolkumar/health-insurance-cross-sell-prediction)) and it involves a insurance company's database and contains information about existing customers who were targeted in previous cross-selling campaigns. The dataset includes the following variables:

- Gender: Gender of the customer
- Age: Age of the customer
- Driving License: 0 (Customer does not have DL), 1 (Customer already has DL)
- Region Code: Unique code for the region of the customer
- Previously Insured: 1 (Customer already has Vehicle Insurance), 0 (Customer doesn't have Vehicle Insurance)
- Vehicle Age: Age of the Vehicle
- Vehicle Damage: 1 (Customer got his/her vehicle damaged in the past), 0 (Customer didn't get his/her vehicle damaged in the past)
- Annual Premium: The amount customer needs to pay as premium in the year
- Policy Sales Channel: Anonymized Code for the channel of outreaching to the customer ie. Different Agents, Over Mail, Over Phone, In Person, etc.
- Vintage: Number of Days, Customer has been associated with the company

For training data, the target variable was given by
- Response:  1 (Customer is interested), 0 (Customer is not interested)

## Model
The model used in this project is an XGBoost model that was fine-tuned using a Bayesian optimization approach. The model was trained on the historical data obtained from previous campaigns, and the output is a ranking score that ranks the customers by their probability of purchase. As the main problem is to sort the list of clients the metrics [Cumulative Gain Curve](http://mlwiki.org/index.php/Cumulative_Gain_Chart) and [Lift Curves](https://www.geeksforgeeks.org/understanding-gain-chart-and-lift-chart/) were used to assess model performance. 

Also, assuming a traditional threshold of 0.5, this model can be seen as a classification model, so [ROC and AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc?hl=en) metrics are also used (and thus these were the initial assessment method on Kaggle's original competition). 

The selected model performed consistently higher on all considered metrics (metrics for other considered models are available on notebooks) and thus was selected for deployment. 

<img src="models/figures/xgboost_finetuned.png" width="900" height="300" />

## API
The model was deployed through a FastAPI API that is hosted on Render. The API accepts a JSON file containing the variables for each customer and returns a JSON file containing the ranking score for each customer. The API was tested using Pytest. Tests are still to be included in the repository.

## Project Deployment

The general overview for the deployment of this project is presented as follows: 

<img src="project_architecture.png" width="600" height="400" />






