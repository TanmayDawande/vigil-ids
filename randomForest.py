from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np

datasets = {
    1: 'data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv',
    2: 'data/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv',
    3: 'data/Wednesday-workingHours.pcap_ISCX.csv'
}

def cleaner(file_path):
    df = pd.read_csv(file_path)
    df = df.drop_duplicates()
    #remove all spaces
    df.columns = df.columns.str.strip()
    #clean the -inf and inf values
    df = df.replace([np.inf, -np.inf], np.nan)
    #drops missing values
    df = df.dropna(axis = 0)
    #remove all spaces
    df.columns = df.columns.str.strip()
    df['Label'] = df['Label'].apply(lambda x: 0 if x == "BENIGN" else 1)
    return df

def train_test(train_dataset, test_dataset):

    df_train = cleaner(train_dataset)
    df_test = cleaner(test_dataset)
    #training the model on what to predict
    y_train = df_train.Label
    #test prediction
    y_test = df_test.Label
    #the data with which y is predicted
    model_features = ['Destination Port', 'Flow Duration', 'Total Fwd Packets' , 'Total Backward Packets', 'Total Length of Fwd Packets' ,'Total Length of Bwd Packets' ,'Fwd Packet Length Max']
    X_train = df_train[model_features]
    X_test = df_test[model_features]
    new_model = RandomForestClassifier(random_state = 0, n_jobs=-1)
    new_model.fit(X_train, y_train)
    print(new_model.predict(X_test))
    predictions = new_model.predict(X_test)

    #--------------------------------------------------------------------
    #confusion matrix display
    print("The confusion matrix is: ")
    cm = confusion_matrix(y_test, predictions, labels=[0, 1])
    print(cm)
    tn, fp, fn, tp = cm.ravel()
    #--------------------------------------------------------------------
    accuracy = ((tp+tn)/(tp+tn+fp+fn))*100
    print(f"the accuracy is {accuracy}%")
    #--------------------------------------------------------------------
    #share of attacks caught
    precision = (tp/(tp+fp))*100
    print(f"The precision is: {precision} %")
    #--------------------------------------------------------------------
    false_alarm_rate = (fp / (fp + tn))*100
    print(f"The false alarm rate is: {false_alarm_rate} %")
    #--------------------------------------------------------------------
    recall = (tp / (tp + fn))*100
    print(f"The recall is: {recall} %")

def test_runner():
    print("--------TEST BEGINNING--------")
    for x in range(1, 4):
        for y in range(1, 4):
            if(x == y): continue
            print(f"### Testing for dataset {x} as training and {y} as test: ")
            train_test(datasets[x], datasets[y])
            print("-------- TEST DONE --------")


if __name__ == "__main__":
    test_runner()

