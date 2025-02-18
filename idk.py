import requests
import pandas as pd
import os

SONARCLOUD_TOKEN = "82a8fe6df3b0391119aa62fd413df6db3707e9b1"
ORGANIZATION_KEY = "gamify"
PROJECT_KEY = "dimp170_refined-sonar-analysis"
HEADERS = {"Authorization": f"Bearer {SONARCLOUD_TOKEN}"}

full_results = []
snippet_results = []

def get_sonar_files():
    sonar_files = {}
    page = 1

    while True:
        url = f"https://sonarcloud.io/api/components/tree"
        params = {
            "component": PROJECT_KEY,
            "qualifiers": "FIL",
            "organization": ORGANIZATION_KEY,
            "p": page,
            "ps": 500
        }

        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            components = response.json().get("components", [])
            file_paths = [c["path"] for c in components]
            print(f"SonarCloud Retrieved Files (First 5): {file_paths[:5]}")
            return {c["path"]: c["key"] for c in components}
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            break



sonar_files = get_sonar_files()
print(f"Retrieved {len(sonar_files)} indexed files from SonarCloud.")


dataset_path = "github_code_dataset_no_comments.csv"
try:
    df = pd.read_csv(dataset_path)
except FileNotFoundError:
    print(f"Error: Dataset file '{dataset_path}' not found.")
    exit()


df["file_path"] = df["file_path"].apply(lambda x: x.split("/")[-1])
df["file_path"] = df["file_path"].apply(lambda x: f"{PROJECT_KEY}:{x}")
df["file_path"] = df["file_path"].apply(lambda x: x.replace(f"{PROJECT_KEY}:", ""))


df["file_path"] = df["file_path"].apply(lambda x: f"{PROJECT_KEY}:{x}" if not x.startswith(PROJECT_KEY) else x)
print(f"Updated Dataset File Paths (First 5): {df['file_path'].head().tolist()}")

df["sonar_component_key"] = df["file_path"].map(sonar_files)


df_filtered = df.dropna(subset=["sonar_component_key"])
print(f"Matched {len(df_filtered)} files to SonarCloud.")



def get_all_sonar_metrics(component_key):
    if not component_key or pd.isna(component_key):
        return {}

    url = "https://sonarcloud.io/api/measures/component"
    params = {
        "component": component_key,
        "organization": ORGANIZATION_KEY,
        "metricKeys": "code_smells,complexity,security_rating,cognitive_complexity,duplicated_lines_density,bugs,vulnerabilities,ncloc"

    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        measures = response.json().get("component", {}).get("measures", [])
        metrics = {m["metric"]: m["value"] for m in measures}


        print(f"SonarCloud Metrics for {component_key}: {metrics}")

        return metrics
    else:
        print(f"API Error ({component_key}): {response.status_code} - {response.text}")
        return {}
def get_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        full_code = f.read()
        snippet = "\n".join(full_code.split("\n")[:5]) + "..."
        return full_code, snippet




sonar_results_all_metrics = {}
for file_path, component_key in sonar_files.items():
    clean_file_name = os.path.basename(file_path)
    full_code, snippet = get_code(file_path)
    metrics = get_all_sonar_metrics(component_key)

    full_row = {
        "file_name": clean_file_name,
        "full_code": full_code
    }
    full_row.update(metrics)
    full_results.append(full_row)

    snippet_row = {
        "file_name": clean_file_name,
        "snippet": snippet
    }
    snippet_row.update(metrics)
    snippet_results.append(snippet_row)

df_full = pd.DataFrame(full_results)
df_snip = pd.DataFrame(snippet_results)

df_full.to_csv("refined-sonar-metrics-for-ai.csv")
df_snip.to_csv("refined-sonar-metrics.csv")







