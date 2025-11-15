import pandas as pd

df = pd.read_csv("weather.csv")
print("Column names in your dataset:")
print(df.columns.tolist())
