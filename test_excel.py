import pandas as pd

file_path = r"D:\Desktop\all-india-villages-master-list-excel\dataset\Rdir_2011_11_SIKKIM.xls"

df = pd.read_excel(file_path)

print("Rows:", len(df))
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())