from transformers import AutoModelForCasualLM, AutoTokenizer
import torch
import pandas as pd

model_name = "bigcode/starcoder"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCasualLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

df = pd.read_csv("sonarcloud_metrics.csv")

if "optimized_code" not in df.columns:
    df["optimized_code"] = ""

def op_code(code_snippet):
    prompt = f"Optimize the following Python code for better readability and efficiency:\n\n{code_snippet}"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length)