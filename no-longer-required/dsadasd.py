import pandas as pd
import os

# ✅ Load the dataset
OPTIMIZED_CSV = "final_optimized_complex_code.csv"
df_optimized = pd.read_csv(OPTIMIZED_CSV)

# ✅ Create the repo directory
OPTIMIZED_REPO_DIR = "../optimized_complex_repo"
os.makedirs(OPTIMIZED_REPO_DIR, exist_ok=True)

# ✅ Save each optimized script as a `.py` file
for _, row in df_optimized.iterrows():
    file_name = row["file_name"]  # Get file name
    optimized_code = row["full_code"]  # Optimized code

    # ✅ Define full file path
    file_path = os.path.join(OPTIMIZED_REPO_DIR, file_name)

    # ✅ Write the optimized code to a Python file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(optimized_code)

print(f"✅ Optimized repo created with {len(df_optimized)} Python files in '{OPTIMIZED_REPO_DIR}'.")





