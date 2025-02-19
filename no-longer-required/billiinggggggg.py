import pandas as pd

# ✅ Load the dataset
df = pd.read_csv("optimized_part2.csv")

# ✅ Identify rows where 'optimized_code' is the same as 'full_code'
df_remaining = df[df["optimized_code"] == df["full_code"]]

# ✅ Save only unoptimized rows

df_remaining.to_csv("remaining_unoptimized.csv", index=False)
print(f"✅ {len(df_remaining)} code snippets were NOT actually optimized and need to be reprocessed.")


