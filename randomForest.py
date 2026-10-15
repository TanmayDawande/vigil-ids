from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

dataset1 = 'data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'
dataset2 = 'data/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv'
dataset3 = 'data/Wednesday-workingHours.pcap_ISCX.csv'

df1 = pd.read_csv(dataset1)
df2 = pd.read_csv(dataset2)
df3 = pd.read_csv(dataset3)

df = pd.concat([df1, df2, df3])

#remove all spaces
df.columns = df.columns.str.strip()

df['Label'] = df['Label'].apply(lambda x: 0 if x == "BENIGN" else 1)

#drops missing values
df = df.dropna(axis = 0)

#what to predict using the data
y = df.Label

#the data with which y is predicted
model_features = ['Destination Port', 'Flow Duration', 'Total Fwd Packets' , 'Total Backward Packets', 'Total Length of Fwd Packets' ,'Total Length of Bwd Packets' ,'Fwd Packet Length Max']

X = df[model_features]

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)

new_model = RandomForestClassifier(random_state = 0, n_jobs=-1)
new_model.fit(train_X, train_y)

joblib.dump(new_model, 'models/virgil-brains.pkl')
print("Model trained and saved")

