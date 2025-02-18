import pandas as pd
dataset_path = "github_code_dataset_with_efficiency_scores.csv"
df = pd.read_csv(dataset_path)


columns_to_remove = ["efficiency_score"]
df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")


final_file_path = "github_code_dataset_no_comments.csv"
df.to_csv(final_file_path, index=False)