import glob
import pandas as pd
import numpy as np
import os

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
    df['attack'] = df['Label'].str.strip().str.replace(r'[^\x00-\x7F]+', '-', regex=True)
    file_name = os.path.basename(file_path)
    df['day'] = (file_name.split('-', 1))[0]
    df['source_file'] = file_name
    df['Label'] = (df['attack'] != 'BENIGN').astype(int)
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
print(check['day'].value_counts())
