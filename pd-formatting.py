import pandas as pd

df = pd.read_csv("messy_python_dataset.csv")
df = df.drop("repo_name", axis=1)
df = df.drop("file_size", axis=1)
df = df.drop("file_url", axis=1)

df.to_csv("formatted_messy_python_data.csv", index=False)