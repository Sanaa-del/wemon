import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Function to load the JSON data
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Function to normalize and flatten the JSON data
def normalize_data(data):
    # Flatten the JSON structure and create a DataFrame
    df = pd.json_normalize(data)
    return df

# Function to treat and analyze each measurement
def treat_and_analyze(data):
    if data is None or not isinstance(data, pd.DataFrame):
        print("Invalid data. Please check the input file and try again.")
        return

    # Display the first few rows of the dataset
    print("First few rows of the dataset:")
    print(data.head())

    # Display the summary information of the dataset
    print("\nDataset info:")
    print(data.info())

    # Create histograms for each numerical column
    for column in data.columns:
        if data[column].dtype in ['int64', 'float64']:  # Only process numerical columns
            print(f"\nCreating histogram for column: {column}")
            
            # Handle missing values (example: fill with the mean value)
            data[column].fillna(data[column].mean(), inplace=True)
            
            # Create histogram
            plt.figure(figsize=(10, 5))
            sns.histplot(data[column], kde=True)
            plt.title(f'Histogram of {column}')
            plt.show()

# Main script
file_path = '/home/sghandi/Téléchargements/wemon-main/LWIP.Metrics.json'
data = load_json_data(file_path)
if data:
    df = normalize_data(data)
    treat_and_analyze(df)

