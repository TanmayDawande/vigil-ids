# results

last updated: 2026-10-18

## setup

- **data:** CIC-IDS-2017 (MachineLearningCSV). three files, each used whole:
  - **DDoS:** friday afternoon, called 1 below
  - **PortScan:** friday afternoon, called 2 below
  - **wednesday:** DoS family attacks, called 3 below
- **cleaning (same for every file):** strip the column names, turn infinity into blank, drop rows with blanks, drop duplicate rows, label 0 for BENIGN and 1 for any attack.
- **model:** scikit-learn `RandomForestClassifier`, default settings, `random_state=0`.
- **features (7):** Destination Port, Flow Duration, Total Fwd Packets, Total Backward Packets, Total Length of Fwd Packets, Total Length of Bwd Packets, Fwd Packet Length Max.
- **split:** by file. train on one file, test on a different one. no shuffled split, so no near-identical flows leak from train into test.

## experiment 1: train on one file, test on another (with destination port)

| train | test | attacks caught (recall) | false alarm rate | precision | accuracy |
|---|---|---|---|---|---|
| DDoS | PortScan | 0.06% | 0.06% | 43.08% | 57.57% |
| DDoS | wednesday | 1.40% | 0.07% | 90.74% | 68.66% |
| PortScan | DDoS | 14.82% | 0.01% | 99.96% | 51.12% |
| PortScan | wednesday | 2.11% | 0.01% | 98.89% | 68.93% |
| wednesday | DDoS | 40.23% | 0.62% | 98.87% | 65.44% |
| wednesday | PortScan | 0.38% | 0.25% | 52.30% | 57.59% |

### raw confusion matrix counts

| train | test | true negatives | false positives | false negatives | true positives |
|---|---|---|---|---|---|
| DDoS | PortScan | 123,009 | 74 | 90,638 | 56 |
| DDoS | wednesday | 416,459 | 277 | 191,041 | 2,715 |
| PortScan | DDoS | 95,061 | 7 | 109,041 | 18,973 |
| PortScan | wednesday | 416,690 | 46 | 189,662 | 4,094 |
| wednesday | DDoS | 94,482 | 586 | 76,517 | 51,497 |
| wednesday | PortScan | 122,772 | 311 | 90,353 | 341 |

## how to read the columns

- **attacks caught (recall):** out of the real attacks in the test file, how many the model flagged. `TP / (TP + FN)`. this is the number that matters most.
- **false alarm rate:** out of the real normal flows, how many the model wrongly called attacks. `FP / (FP + TN)`.
- **precision:** out of the flows the model flagged, how many really were attacks. `TP / (TP + FP)`. it can look great even when recall is terrible.
- **accuracy:** share of all flows classified correctly. it can look fine even when the model misses almost every attack.

## notes

these numbers are pretty bad, and that is the main finding so far. a random forest trained only on the DDoS file caught 56 port scan attacks and missed 90,638, so a model that only knows one kind of attack is basically blind to a different one. the best result was wednesday to DDoS at 40%, probably because both are flood style DoS attacks. accuracy can look okay while the model misses almost every attack, so recall is the number to watch. this is one model on 7 features and three files, so it shows what this setup can't do, not what every firewall can't do.