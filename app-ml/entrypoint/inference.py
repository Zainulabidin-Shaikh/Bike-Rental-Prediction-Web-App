"""
Inference Pipeline:
- Loads configuration
- Initializes production database
- Loops through a given number of timestamps and runs inference
- Saves predictions
- Plots comparison of predicted vs actual values
"""

import os
import sys
from pathlib import Path
import pandas as pd
import sys
print(sys.executable) # this print running script's Python executable path
# Note: The print statement above is for debugging purposes to show the Python executable path.
# It can be removed in production code.
# The path printed by sys.executable is useful for understanding which Python environment is being used.
"""
sys.executable is a Python variable (from the built-in sys module) 
that gives you the full absolute path to the 
Python interpreter executable that is currently running your code.
"""

# Set the project root directory
# This assumes the script is located at app-ml/entrypoint/inference.py
# and the project root is two levels up from this script.
project_root = Path(__file__).resolve().parents[2]
os.chdir(project_root)
# changing the current working directory to the project root
# This is useful for ensuring that relative paths in the code work correctly.
# print(f"Current working directory changed to: {os.getcwd()}")
sys.path.append(str(project_root))
# Add the src directory to the Python path
# This allows importing modules from the src directory without needing to specify the full path.
sys.path.append(str(project_root / 'app-ml' /'src'))
# adding src directory to the Python path

from common.utils import read_config, plot_predictions_vs_actual
# importing utility functions for reading configuration files
# and plotting predictions vs actual values.
# read_config is used to load the configuration file,
# and plot_predictions_vs_actual is used to visualize the results.
from pipelines.pipeline_runner import PipelineRunner
# importing the PipelineRunner class which is responsible for running the inference pipeline
# The PipelineRunner class encapsulates the logic for running the inference pipeline,
# including loading data, running models, and saving predictions.
# It is initialized with a configuration object and a DataManager instance.

from common.data_manager import DataManager
# The DataManager is responsible for handling data loading and saving operations.
# It abstracts the details of data management, allowing the PipelineRunner to focus on the inference logic.


if __name__ == "__main__":
    # Number of runs for
    num_timestamps = 200
    # we are running inference for 200 timestamps because
    # the dataset is large and we want to process it in chunks.
    # This allows us to manage memory usage and processing time effectively.

    print("Starting inference pipeline...")

    # Load config file
    config_path = project_root / 'config' / 'config.yaml'
    config = read_config(config_path)

    # Ensure the config is loaded correctly
    # we load config files to get the necessary parameters for the pipeline
    # such as data paths, model parameters, etc.

    # Initialize data manager and timestamps
    # The DataManager handles data loading and saving
    # data manager is responsible for managing the data flow in the pipeline
    # including loading data from the production database,
    # saving predictions, and loading actual data for comparison.
    # print("Initializing DataManager...")

    data_manager = DataManager(config)
    current_timestamp = pd.to_datetime(config['pipeline_runner']['first_timestamp'])
    # the above line initializes the current timestamp
    # from the configuration file, which specifies the starting point for inference.
    # This timestamp will be incremented in each iteration of the loop.
    
    # Time increment for each step
    # Thi is used to move to the next timestamp in each iteration
    # The time increment is defined in the configuration file
    # and is used to determine how much to advance the timestamp after each inference run.
    time_increment = pd.Timedelta(config['pipeline_runner']['time_increment'])
    # timedelta is a pandas function that represents a duration, the difference between two dates or times.
    # example use of timedelta:
    # from datetime import timedelta
    # time_increment = timedelta(minutes=5)  # Increment by 5 minutes

    # Prepare production database
    data_manager.initialize_prod_database()
    # The initialize_prod_database method sets up the production database
    # This may involve creating necessary tables, loading initial data, or preparing the environment for inference.
    # It ensures that the database is ready to store predictions and other results.

    # Initialize Pipeline Runner
    pipeline_runner = PipelineRunner(config=config, data_manager=data_manager)
    
    # Load the dataset to run inference on
    dataset_path = os.path.join(
        config['data_manager']['prod_data_folder'],
        config['data_manager']['real_time_data_prod_name']
    )
    df = data_manager.load_data(dataset_path)

    # Loop through timestamps
    for i in range(num_timestamps):
        print(f"Processing timestamp {i+1}/{num_timestamps}: {current_timestamp}")

        # Run inference on this timestamp's data
        pipeline_runner.run_inference(current_timestamp)
        
        # Increment timestamp
        current_timestamp += time_increment
    
    print("Inference completed for all timestamps!")
    
    # Load predictions and actual data for plotting
    print("Loading data for plotting...")
    predictions_df = data_manager.load_prediction_data()
    actual_df = data_manager.load_prod_data()
    plot_predictions_vs_actual(predictions_df, actual_df)