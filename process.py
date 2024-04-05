import os, yaml
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

global_parameters = yaml.safe_load(open('params.yaml'))['global']
parameters = yaml.safe_load(open('params.yaml'))['process']

################################################ Variables ################################################
dir_download = global_parameters['dir_download']
hourly_cols = global_parameters['hourly_cols']
GT_cols = global_parameters['cols_filter']
GT_to_hourly = {gt:hourly for gt,hourly in zip(GT_cols,hourly_cols)}
calc_dir = os.path.join(*parameters['calc_dir'])

os.makedirs(calc_dir, exist_ok=True)

# Get list of CSV files in the directory
csv_files = [file for file in os.listdir(dir_download) if file.endswith('.csv')]
dfs = []

for i,filename in enumerate(csv_files):
    download_path = os.path.join(dir_download, filename)
    df = pd.read_csv(download_path, low_memory=False)  # Read the downloaded CSV file into DataFrame

    df['Month'] = df['DATE'].apply( lambda x: int(x.split('-')[1]) )  
    df.drop('DATE',axis=1,inplace=True)

    # The below code filters out the columns which contain the monthly average data for ground truth
    GT_df = df[['Month']+GT_cols].groupby('Month').tail(1).dropna(axis=1,thresh=1).reset_index(drop=True)

    valid_hourly = [GT_to_hourly[col] for col in list(GT_df.columns)[1:]]

    # Function to handle potential "s" suffix
    def convert_to_float(value):
        if type(value) == str:
            return float(value.rstrip('s'))  
        else: 
            return value

    # Apply the conversion function to pressure columns
    for col in valid_hourly:
        df[col] = df[col].apply(convert_to_float)

    calc_avgs = df[["Month"] + valid_hourly]

    # Get the calculated monthly averages
    calc_avgs_df = calc_avgs.groupby('Month')[valid_hourly].mean().reset_index()
    calc_avgs_df.to_csv( os.path.join(calc_dir, f'calc_csv_{i+1}.csv'),index=False)