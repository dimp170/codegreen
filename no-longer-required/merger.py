import pandas as pd

# ✅ Load all three parts
df_part1 = pd.read_csv("optimized_part1.csv")
df_part2 = pd.read_csv("optimized_part2.csv")
df_part3 = pd.read_csv("optimized_part3.csv")

# ✅ Merge into a single dataset
df_final = pd.concat([df_part1, df_part2, df_part3])

# ✅ Save the fully optimized dataset
df_final.to_csv("final_training_optimized.csv", index=False)

print("✅ Merged optimized dataset saved as 'final_training_optimized.csv'.")
