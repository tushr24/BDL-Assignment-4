import os, yaml
import pandas as pd
import warnings
from sklearn.metrics import r2_score
warnings.filterwarnings('ignore')

parameters = yaml.safe_load(open('params.yaml'))

################################################ Variables ################################################
get_dir = os.path.join(*parameters['prepare']['get_dir'])
calc_dir = os.path.join(*parameters['process']['calc_dir'])
get_csvs = [file for file in sorted(os.listdir(get_dir)) if file.endswith('.csv')]
calc_csvs = [file for file in sorted(os.listdir(calc_dir)) if file.endswith('.csv')]

r2_df = pd.DataFrame(columns=pd.read_csv(os.path.join(get_dir, get_csvs[0])).columns[1:])
for gt,calc in zip(get_csvs,calc_csvs):

    GT_df = pd.read_csv( os.path.join(get_dir,gt))
    calc_avgs_df = pd.read_csv( os.path.join(calc_dir,calc))

    # Handle missing values (NA) in ground truth
    GT_df_dropna = GT_df.dropna()  # Drop rows with NA in ground truth
    calc_avgs_dropna = calc_avgs_df.iloc[GT_df_dropna.index]  # Select corresponding rows in predictions

    # Calculate R2 score for each column
    r2_scores = []
    for col_num in range(1,len(GT_df_dropna.columns)):
        r2_scores.append(r2_score(GT_df_dropna.iloc[:,col_num], calc_avgs_dropna.iloc[:,col_num]))

    r2_df.loc[calc] = r2_scores
r2_df.to_csv('R2results.csv')