# vigil-ids

a machine learning network intrusion detector, trained and tested on the CIC-IDS-2017 dataset. work in progress.

the goal is to flag attack traffic and to measure honestly how well that works, including on attack types the model never saw during training.

## status

- done: cleaning and combining the raw data (`prepare.py`), and a cross-file evaluation of a random forest (`randomForest.py`)
- done: add day and attack name columns, split train and test by day, better features, a tuned alert threshold, isolation forest for unseen attacks

## data

CIC-IDS-2017 (MachineLearningCSV version): 8 csv files, one per time slot of a week of traffic on a test network. each row is one network flow, described by 78 numeric features and a label. the raw files are not in this repo. download them and put them in `data/`.

after cleaning: 2,572,640 rows, of which 2,146,899 are normal and 425,741 are attacks.

## what prepare.py does

for each csv in `data/`:

- read it with the cp1252 encoding (one label contains a non-standard dash)
- drop duplicate rows
- strip spaces from the column names
- turn infinity values into blanks, then drop rows with blanks
- label each row 0 for BENIGN or 1 for any attack

then it combines all 8 files and saves the result as `data/clean.parquet`.

## evaluation

`randomForest.py` trains a random forest on one of three files (DDoS, PortScan, Wednesday) and tests it on each of the others. splitting by file, instead of shuffling rows, stops near-identical flows from leaking from train into test. the results are in `notes/results.md`. short version: a model trained on one attack type usually catches very little of a different type.

## run

```
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy scikit-learn pyarrow joblib
python prepare.py
python randomForest.py
```