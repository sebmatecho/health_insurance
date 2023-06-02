import pandas as pd 
import pickle
import os
from  pathlib import Path

class HealthInsurance(): 
    def __init__(self)->None:
        base_path = Path.cwd().parent
        # print(base_path)
        self.home = base_path/'parameters'
        self.age_transform = pickle.load(open(os.path.join(self.home,'age_transform.pkl'),'rb'))
        self.annual_premium_transform = pickle.load(open(os.path.join(self.home,'annual_premium_transform.pkl'),'rb'))
        self.gender_transform = pickle.load(open(os.path.join(self.home,'gender_transform.pkl'),'rb'))
        self.policy_sales_channel_transform = pickle.load(open(os.path.join(self.home,'policy_sales_channel_transform.pkl'),'rb'))
        self.region_code_transform = pickle.load(open(os.path.join(self.home,'region_code_transform.pkl'),'rb'))
        self.vintage_transform = pickle.load(open(os.path.join(self.home,'vintage_transform.pkl'),'rb'))
        
    def data_cleaning(self,df1): 
                
        df1.columns = ['gender', 'age', 'driving_license', 'region_code', 'previously_insured',
       'vehicle_age', 'vehicle_damage', 'annual_premium','policy_sales_channel', 'vintage']
        
        df1['age'] = df1['age'].astype(int)
        df1['driving_license'] = df1['driving_license'].astype(int)
        df1['region_code'] = df1['region_code'].astype(int)
        df1['previously_insured'] = df1['previously_insured'].astype(int)
        df1['vintage'] = df1['vintage'].astype(int)
        
        return df1
    
    def feature_engineering(self,df2): 
        df2['vehicle_damage'] = df2['vehicle_damage'].apply( lambda x: 1 if x == 'Yes' else 0 )
        df2['vehicle_age'] =  df2['vehicle_age'].apply( lambda x: 'over_2_years' if x == '> 2 Years' else 'between_1_2_year' if x == '1-2 Year' else 'below_1_year' )
        return df2
    
    def data_preparation(self, df3): 
        df3['annual_premium'] = self.annual_premium_transform.transform( df3[['annual_premium']].values )
        df3['age'] = self.age_transform.transform( df3[['age']].values )
        df3['vintage'] = self.vintage_transform.transform( df3[['vintage']].values )
        df3['gender'] = df3['gender'].map( self.gender_transform )
        df3['region_code'] = df3['region_code'].map( self.region_code_transform )
        df3 = pd.get_dummies( df3, prefix='vehicle_age', columns=['vehicle_age'] )
        df3['policy_sales_channel'] = df3['policy_sales_channel'].map( self.policy_sales_channel_transform )
        
        cols_selected = ['annual_premium', 'vintage', 'age', 'region_code', 'vehicle_damage', 'previously_insured',
                 'policy_sales_channel']
    
        return df3[cols_selected]
    
    def prediction(self,model, df4, df5): 
        pred = model.predict_proba(df4)
        df5['score'] = pred[:, 1]
        return df5
