"""
Training Pipeline:
- Loads configuration
- Initializes production database
- Runs the full training pipeline (preprocessing, feature engineering, training, postprocessing)
- Saves the trained model to the models folder
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
"""
🧩 What is sys.path?

sys.path is a list of directories where Python looks for modules when you use import.

🧩 What does sys.path.append(...) do?

Adds a new directory to sys.path.

After this, Python will look for modules in that directory when importing.

🧩 Why append project_root?

Ensures that Python can find modules in the root directory of your project.

For example, if you have a module like common.utils, Python needs to know where to find it.

"""
sys.path.append(str(project_root / 'app-ml' /'src'))
os.chdir(project_root) # Change directory to read the files from ./data folder


from common.utils import read_config
from pipelines.pipeline_runner import PipelineRunner
from common.data_manager import DataManager


if __name__ == "__main__":

    # Load config file
    config_path = project_root / 'config' / 'config.yaml'
    config = read_config(config_path)

    # Initialize production database with historical raw data
    data_manager = DataManager(config)
    data_manager.initialize_prod_database()

    # Initialize Pipeline Runner
    pipeline_runner = PipelineRunner(config=config, data_manager=data_manager)

    # Run the training pipeline
    pipeline_runner.run_training()


"""
🧱 1. data_manager = DataManager(config)

💡 What it does:

This creates a "data manager" — like a librarian for your data.

It’s an object (a smart helper) that knows how to:

Find raw data
Clean it
Save it in the right place

It uses the config.yaml file to know:

Where the data is (./data/raw_data/)
What to name it (database.parquet)
Which columns to drop, rename, etc.

🎯 Analogy:

Think of DataManager as a robot assistant who says:
"I read the instructions (config), and now I know how to organize your data." 

📦 2. data_manager.initialize_prod_database()

💡 What it does:

This tells the data manager to:

"Take the raw historical data (like CSV files), clean it, and save it as a clean production-ready database." 

It does things like:

Rename columns (e.g., yr → year)
Drop useless columns (like casual, registered)
Handle missing values
Save the clean data as database_prod.parquet (a fast, efficient format)

🎯 Analogy:

You have a messy closet full of clothes.

This line says:

"Robot, take all my clothes, fold them, throw away the old ones, and put the good ones in a neat drawer."
Now your closet is ready to use. 

🏗️ 3. pipeline_runner = PipelineRunner(config=config, data_manager=data_manager)

💡 What it does:

This creates a "pipeline runner" — like a project manager for your ML workflow.

It knows the whole process from start to finish:

Load clean data
Create features (like lag features)
Train the model
Save the model

It uses:

config → to know what to do (e.g., which lags to create)
data_manager → to get the clean data

🎯 Analogy:

The PipelineRunner is like a construction site manager who says:
"I have the blueprint (config) and the materials (from data_manager). Now I’ll build the house (train the model)." 

🚀 4. pipeline_runner.run_training()

💡 What it does:

This is the big red button — it starts the entire training process.

It will:

Load the clean data (from data_manager)
Create lag features (e.g., "What was the bike count 1 hour ago?")
Split into train/validation
Use Optuna to find the best CatBoost settings
Train the final model
Save the model to models/prod/latest_model

🎯 Analogy:

You’ve hired workers, gathered materials, and made a plan.

This line says:

"Start building the house!"
And it all happens automatically. 
"""