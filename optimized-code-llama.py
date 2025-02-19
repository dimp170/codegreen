import requests
import pandas as pd
from tqdm import tqdm
import numpy as np


API_KEY = "konwrGfXQpQofWTS2WfT1NpPU8XmvHhn"


def optimize_code(code_snippet):


    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "messages": [
            {"role": "system", "content": "Optimize this Python code for efficiency and readability."},
            {"role": "user", "content": code_snippet}
        ],
        "max_tokens": 4000
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return code_snippet



df = pd.read_csv("complex_code_dataset.csv")





tqdm.pandas(desc="Optimizing Code")
df["optimized_code"] = df["full_code"].progress_apply(optimize_code)


df.to_csv("optimized_complex.csv", index=False)
print("Optimized dataset saved as 'optimized_part3.csv'")