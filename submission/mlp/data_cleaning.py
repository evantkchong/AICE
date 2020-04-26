#!/usr/bin/python3
import pandas as pd

'''
A Simple module that replicates the cleaning steps
performed in eda.ipynb for the pipeline.
'''

def fix_weather(df):
    correction_dict = {
    'lear':'clear',
    'clar':'clear',
    'loudy':'cloudy',
    'cludy':'cloudy',
    'liht snow/rain':'light snow/rain'
    }
    df["weather"] = df["weather"].str.lower()
    df["weather"].replace(correction_dict, inplace=True)

    # Now we convert the field into a categorical field
    df["weather"] = df["weather"].astype('category')
    return df

def fix_date(df):
    df['date'] = pd.to_datetime(df['date'], utc=False)
    return df

def one_hot_encode_column(df, column):
    ohe = pd.get_dummies(df[[column]])
    new_df = pd.concat([df, ohe], axis=1)
    return new_df

def clean_all(df):
   df = fix_weather(df)
   df = fix_date(df)
   new_df = one_hot_encode_column(df, 'weather')
   return new_df