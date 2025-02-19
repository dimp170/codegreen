import pandas as pd


dataset_path = "../csv-Data/github_code_dataset_with_all_sonar_metrics.csv"
df_final = pd.read_csv(dataset_path)


columns_to_drop = ["repo_name", "file_path", "sonar_component_key"]


df_final = df_final.drop(columns=[col for col in columns_to_drop if col in df_final.columns], errors="ignore")
df_final = df_final[df_final["short_code_snippet"].notna() & (df_final["short_code_snippet"].str.strip() != "")]

updated_file_path = "../csv-Data/sonarcloud_metrics.csv"
df_final.to_csv(updated_file_path, index=False)

df = pd.read_csv("../csv-Data/sonarcloud_metrics.csv")

# Create blank rows
blank_row = pd.DataFrame([[""] * len(df.columns)], columns=df.columns)

# Insert a blank row after every row
df_spaced = pd.concat([pd.concat([df.iloc[[i]], blank_row]) for i in range(len(df))], ignore_index=True)

# Save the updated dataset
df_spaced.to_csv("sonar_metrics.csv", index=False)

