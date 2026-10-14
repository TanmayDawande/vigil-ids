from sklearn.tree import DecisionTreeRegressor
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

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    new_model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state = 0)
    new_model.fit(train_X, train_y)

    val_predictions = new_model.predict(val_X)
    return (mean_absolute_error(val_y, val_predictions))

for max_leaf_nodes in [2, 3, 5, 8, 12, 20, 50]:
    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %.6f" %(max_leaf_nodes, my_mae))
