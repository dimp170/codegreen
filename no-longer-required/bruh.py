import pandas as pd

# ✅ Load the dataset
df = pd.read_csv("optimized_part2.csv")


df_part2 = df[df["optimized_code"] != df["full_code"]]
# ✅ Save only unoptimized rows
df_part2.to_csv("optimized_part2.csv", index=False)
print(f"✅ {len(df_part2)} code snippets were actually optimized and need to be reprocessed.")