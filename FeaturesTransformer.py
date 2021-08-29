import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
import json
import joblib

class FeaturesTransformer:
    
    def __init__(self,
                 category_intersections = "category_intersections.csv",
                 category_json_filename = "category_dictionary.json",
                 model_filename = "regressor_model.pkl",
                 cat_cols = ['BOROUGH', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'ZIP CODE'],
                 str_cols = ['ADDRESS'],
                 num_cols = ['LAND SQUARE FEET', 'GROSS SQUARE FEET', 'YEAR BUILT'],
                 X_cols = ['NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'ZIP CODE', 'LAND SQUARE FEET', 'GROSS SQUARE FEET', 'YEAR BUILT']
                ):
        with open(category_json_filename, "r") as fp:
            self.category_dictionary = json.load(fp)
        self.cat_intersections = pd.read_csv(category_intersections)
        self.model = joblib.load(model_filename)
        self.category_columns = cat_cols
        self.string_columns = str_cols
        self.numeric_columns = num_cols
        self.features_columns = X_cols
        self.df = None
        
    def raw_X_to_df(self, raw_X):
        self.df = pd.DataFrame([raw_X], columns=self.category_columns + self.string_columns + self.numeric_columns)
        for col in self.category_columns:
            self.df[col] = self.df[col].astype(CategoricalDtype(self.category_dictionary[col]))
        self.df[self.string_columns] = self.df[self.string_columns].astype('string')
        self.df[self.numeric_columns] = self.df[self.numeric_columns].astype('int64')        
        
        return self

    def predict_sale_price(self):
        
        return f'{self.model.predict(self.df[self.features_columns])[0]:,.0f} $'
    
    def return_predict_table(self, column_name = 'SALE PRICE'):
        self.df[column_name] = [self.predict_sale_price()]
        
        return self.df