#!/usr/bin/python3

import os
import json
import sklearn
import argparse

from data_extraction import SQLHandler
from data_cleaning import clean_all

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

        self.df = None

    def extract_data(self):
        # Unpack settings from config file into args
        handle = SQLHandler(server=self.config_dict["server"],
                            database=self.config_dict["database"],
                            username=self.config_dict["username"],
                            password=self.config_dict["password"],
                            table_name=self.config_dict["table_name"])
        self.df = handle.extract(year_from=self.config_dict["year_from"],
                                 year_to=self.config_dict["year_to"],
                                 exclude_fields=self.config_dict["exclude_fields"])
        print('Data Extracted')

    def clean_data(self):
        clean_all(self.df)
        print('Data Cleaned')

    def train_eval_model(self):
        print('Model Trained')
        print('Model Evaluated')

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
