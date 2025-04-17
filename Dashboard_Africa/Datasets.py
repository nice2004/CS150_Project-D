import pandas as pd

# Load the datasets
dataset_conflicts = pd.read_csv('../Datasets/number-of-armed-conflicts.csv')
dataset_agriculture = pd.read_csv('../Datasets/value-of-agricultural-production.csv')

print(dataset_agriculture.columns)
print(dataset_conflicts.columns)
print(dataset_agriculture.head())
print(dataset_conflicts.head())

missing_dataset1 = dataset_conflicts.isna().sum()
missing_dataset2 = dataset_agriculture.isna().sum()
print(missing_dataset1, missing_dataset2)
# changing column names
agri_value_col = ('Agriculture | 00002051 || Gross Production Value (current thousand US$) | 000057 || thousand US '
                  'Dollar')


conflict_columns = {
    'one_sided_violence': 'Number of ongoing conflicts - Conflict type: one-sided violence',
    'extra_systemic': 'Number of ongoing conflicts - Conflict type: extrasystemic',
    'non_state_conflict': 'Number of ongoing conflicts - Conflict type: non-state conflict',
    'intrastate': 'Number of ongoing conflicts - Conflict type: intrastate',
    'interstate': 'Number of ongoing conflicts - Conflict type: interstate'
}