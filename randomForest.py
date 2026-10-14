from sklearn.ensemble import RandomForestRegressor  
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd

file_path = 'dataset.csv'
data = pd.read_csv(file_path)

#drops missing values
data = data.dropna(axis = 0)

#what to predict using the data
y = data.duration_s

#the data with which y is predicted
model_features = ['fwd_packets', 'bwd_packets', 'fwd_bytes' , 'bwd_bytes', 'syn_count' ,'dst_port' ,'avg_pkt_size']

X = data[model_features]

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)

new_model = RandomForestRegressor(random_state = 0)
new_model.fit(train_X, train_y)

val_predictions = new_model.predict(val_X)
print(mean_absolute_error(val_y, val_predictions))

