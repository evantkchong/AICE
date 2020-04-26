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

def fix_date(df):
    df['date'] = pd.to_datetime(df['date'], utc=False)

def clean_all(df):
   fix_weather(df)
   fix_date(df)
   return df