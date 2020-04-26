# End to End Machine Learning Pipeline for the AICE (Associate) Technical Test
by *Evan Chong Tze Kai*

> n.b. I would like to apologise for the incomplete submission. Things have been hectic at work recently and I did not have sufficient time to complete the test to an acceptable quality. Nevertheless, thank you for looking at my submission. 


The purpose of this readme is to briefly explain the following:
1. Project Structure
2. Running the Pipeline

---

## 1. Project Structure
In the mlp directory there are four modules `data_cleaning.py`, `data_extraction.py`, `models.py` and `pipeline.py`, cleanly separating code from each step of the pipeline.

`data_cleaning.py` is capable of running as a standalone script to fufill the requirements of `part one` of the Techincal Test. The extraction module is somewhat flexible and can be used with different databases as the SQL query is dynamically generated.

`models.py` contains some simple training/evaluation functions for predicting the number of active e-scooter users. 

`pipeline.py` can also be run as a standalone script with the option of being run with a config.json file for modifying the pipeline (more details later). The `PipelineRunner` class from the `pipeline` module can also be used as part of a larger project.


## 2. Running the Pipeline

Running the pipeline, (after setting up the correct python environment with `requirements.txt`) is done with the `run.sh` script.

The `run.sh` script defaults to using the `config.json` file in the submission root.
At the same time, your own configuration json file can be passed to the run-script like so: `run.sh /path/to/config.json`

Please see the next section for the config file format.

### 2.1 config.json File Format
Provided in the root of the submission folder is an example config.json containing the following default values for running the pipeline:

```json
	{
    "server": "aice.database.windows.net",
    "database": "aice",
    "username": "aice_candidate",
    "password": "@ic3_a3s0c1at3",
    "table_name": "rental_data",
    "year_from": 2011,
    "year_to": 2012,
    "exclude_fields":[
        "guest_bike",
        "registered_bike"
    ],
    "model":"linear_regression",
    }
```

* `server`, `database`, `username`, `password` and `table_name` - Connection settings for the SQL Database
* `year_from`, `year_to` - Date range for which to filter results from the Database in-query.
* `exclude_fields` - Fields to exclude from the SQL Query
* `model` - Gives the option of using either `linear_regression` or a `perceptron` for predictive modelling.