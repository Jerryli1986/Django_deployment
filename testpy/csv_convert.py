
# pip install xlrd

import pandas as pd
import csv

Path=r"X:\02 FA\02 Work Items\_WI0022 - Map fuel scores VINs\02 DATA LOAD\03 LOAD\AU.xlsx"
df= pd.read_excel(Path)
print(df[0])
csv_Path=r"X:\02 FA\02 Work Items\_WI0022 - Map fuel scores VINs\02 DATA LOAD\03 LOAD\AU.csv"
df.to_csv(csv_Path)