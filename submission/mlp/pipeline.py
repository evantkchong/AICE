#!/usr/bin/python3

import os
import json
import sklearn
import argparse

from data_extraction import SQLHandler
from data_cleaning import clean_all
from models import run_model

def config_parser(json_path):
    try:
        with open(json_path) as f:
            config_dict = json.load(f)
        return config_dict
    except Exception as err:
        print('Invalid JSON path')
        print(err)
        raise err

class PipelineRunner(object):
    def __init__(self, json_path=None):
        if json_path is None:
            json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     'config.json')
        self.config_dict = config_parser(json_path)
        print('Loaded config at {}'.format(json_path))
        self.read_config()
        self.df = None

    def read_config(self):
        '''
        Hide the mess of reading config file values
        into keyword arguments.
        '''
        server_keywords = ['server', 'database', 'username', 'password', 'table_name']
        self.server_configs = dict((k, self.config_dict[k]) for k in server_keywords)

        extract_keywords = ['year_from', 'year_to', 'exclude_fields']
        self.extract_configs = dict((k, self.config_dict[k]) for k in extract_keywords)

    def extract_data(self):
        # Unpack settings from config file into args
        handle = SQLHandler(**self.server_configs)
        self.df = handle.extract(**self.extract_configs)
        print('Data Extracted')

    def clean_data(self):
        self.df = clean_all(self.df)
        print('Data Cleaned')

    def train_eval_model(self):
        # Run model for registered scooters
        X = self.df[['hr',
                     'feels_like_temperature',
                     'relative_humidity',
                     'windspeed',
                     'weather_clear',
                     'weather_cloudy',
                     'weather_heavy snow/rain',
                     'weather_light snow/rain']].to_numpy()
        
        y1 = self.df['guest_scooter'].to_numpy()
        run_model(X, y1)

        # Run model for guest scooters
        y2 = self.df['registered_scooter'].to_numpy()
        run_model(X, y2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the mlp Pipeline')
    parser.add_argument('-c', '--config', dest='config_file',
                        default=None,
                        help='Configuration json file for the pipeline')

    args = parser.parse_args()
    runner = PipelineRunner(json_path=args.config_file)
    runner.extract_data()
    runner.clean_data()
    runner.train_eval_model()
