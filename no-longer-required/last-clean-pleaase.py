import pandas as pd

# ✅ Load the datasets
df_training = pd.read_csv("training_dataset_cleaned.csv")
df_optimized = pd.read_csv("training_optimized_dataset.csv")

# ✅ Sort both datasets alphabetically by file name
df_training = df_training.sort_values(by="file_name").reset_index(drop=True)
df_optimized = df_optimized.sort_values(by="file_name").reset_index(drop=True)

# ✅ Save the sorted datasets
df_training.to_csv("training_unoptimized_dataset.csv", index=False)
df_optimized.to_csv("training_optimized_dataset.csv", index=False)

print("✅ Both datasets have been sorted alphabetically by file name.")

