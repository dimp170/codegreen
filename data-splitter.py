import pandas as pd
import re
from sklearn.model_selection import train_test_split


df = pd.read_csv("csv-Data/refined-sonar-metrics-for-aiv2.csv")


df = df.dropna(subset=["full_code"])
df = df[df["full_code"].apply(lambda x: isinstance(x, str) and x.strip() != "")]


def is_only_comments(code):

    code_lines = code.strip().split("\n")
    comment_lines = [line for line in code_lines if re.match(r"^\s*#.*", line)]  # Lines that start with #
    return len(comment_lines) == len(code_lines)  # True if all lines are comments


df = df[~df["full_code"].apply(is_only_comments)]


if "optimized_code" not in df.columns:
    df["optimized_code"] = ""


train_df, test_df = train_test_split(df, test_size=0.5, random_state=42)


train_df.to_csv("training_dataset.csv", index=False)
test_df.to_csv("test_dataset.csv", index=False)

print(f"Removed purely commented code snippets.")
print(f"Training set: {len(train_df)} samples")
print(f"Test set: {len(test_df)} samples")

