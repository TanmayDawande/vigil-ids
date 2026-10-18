import glob
import pandas as pd
import numpy as np

files = sorted(glob.glob('data/*.csv'))
print('found', len(files), 'files')

list_table = []

def cleaner(file_path):
    df = pd.read_csv(file_path, encoding='cp1252', low_memory=False)
    df = df.drop_duplicates()
    #remove all spaces
    df.columns = df.columns.str.strip()
    #clean the -inf and inf values
    df = df.replace([np.inf, -np.inf], np.nan)
    #drops missing values
    df = df.dropna(axis = 0)
    df['Label'] = df['Label'].apply(lambda x: 0 if x == "BENIGN" else 1)
    return df

print("-------- Starting file cleaning --------")
for path in files:
    print("Reading and cleaning file:")
    list_table.append(cleaner(path))
    print(path)
    print("-------- next file --------")

combined = pd.concat(list_table, ignore_index=True)
combined.to_parquet('data/clean.parquet', index=False)

print("-------- Cleaning done. Reading now --------")
check = pd.read_parquet('data/clean.parquet')
print(len(check))
print(check['Label'].value_counts())
print(check.shape)
