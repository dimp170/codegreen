import pandas as pd
from datasets import Dataset


df = pd.read_csv("training_dataset.csv")


def format_prompt(example):
    return {
        "input": f"Code:\n{example['unoptimized_code']}\nSonar Scores: Complexity={example['complexity_before']}, Code Smells={example['code_smells_before']}, Bugs={example['bugs_before']}\n\nOptimized Code:",
        "output": example["optimized_code"]
    }


dataset = Dataset.from_pandas(df)
dataset = dataset.map(format_prompt, remove_columns=list(df.columns))


dataset.save_to_disk("sonar_finetuning_dataset")

print("Dataset formatted and saved for fine-tuning!")
