import pandas as pd
import re

# ✅ Load the training dataset and cleaned optimized dataset
training_dataset_path = "training_dataset.csv"
optimized_dataset_path = "final_cleaned_optimized_code.csv"

df_training = pd.read_csv(training_dataset_path)
df_optimized = pd.read_csv(optimized_dataset_path)


def clean_triple_quotes(code):
    """Remove triple quotes at the start and end of the optimized code."""
    if pd.isna(code):
        return ""  # Handle NaN values safely

    # 🔹 Remove triple quotes from the start and end
    code = re.sub(r"^'''|'''$", "", code.strip())

    # 🔹 Remove excessive new lines or whitespace
    return code.strip()


# ✅ Apply the function to clean `full_code`
df_optimized["full_code"] = df_optimized["full_code"].apply(clean_triple_quotes)

# ✅ Remove the first row from both datasets
df_training = df_training.iloc[1:].reset_index(drop=True)
df_optimized = df_optimized.iloc[1:].reset_index(drop=True)

# ✅ Save the cleaned datasets
cleaned_training_path = "training_dataset_cleaned.csv"
cleaned_optimized_path = "final_cleaned_optimized_code_v2.csv"

df_training.to_csv(cleaned_training_path, index=False)
df_optimized.to_csv(cleaned_optimized_path, index=False)

print(f"✅ Cleaned training dataset saved as: {cleaned_training_path}")
print(f"✅ Cleaned optimized dataset saved as: {cleaned_optimized_path}")


