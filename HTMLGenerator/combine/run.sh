#!/bin/bash

# Step 1: Activate the virtual environment
echo "Activating virtual environment..."
source ~/venvs/myenv/bin/activate

# Navigate to the project directory
cd ~/Desktop/combine

# Step 2: Install required dependencies (optional if already installed)
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 3: Run the initial Python scripts in sequence
echo "Running SFIA script..."
python3 sfia.py

echo "Running SFIAReader script..."
python3 SFIAReader.py

echo "Running CAIDI script..."
python3 caidi.py

echo "Running A script..."
python3 dataframe_A.py


echo "Running Example D script..."
python3 dataframe_D.py

echo "Running KnowledgeBase script..."
python3 knowledgebase.py

# Step 4: Finally, run the main app.py
echo "Starting the Flask App..."
python3 app.py

echo "Execution completed. Your app should now be running!"
