import pandas as pd

df = pd.read_csv("../csv-Data/refined-sonar-metrics-for-ai.csv")
df["code_length"] = df["full_code"].astype(str).apply(len)
df_filtered = df[df["code_length"] <= 8192]
df_filtered = df_filtered.drop(columns=["code_length"])

df_filtered.to_csv("refined-sonar-metrics-for-aiv2.csv", index=False)