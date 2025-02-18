import requests
import pandas as pd
import time

SONARCLOUD_TOKEN = "82a8fe6df3b0391119aa62fd413df6db3707e9b1"
ORGANIZATION_KEY = "gamify"
PROJECT_KEY = "dimp170_sonar-analysis-dataset"
HEADERS = {"Authorization": f"Bearer {SONARCLOUD_TOKEN}"}


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
            if not components:
                break


            print(f"SonarCloud Retrieved Files (First 5): {[c['path'] for c in components[:5]]}")


            for c in components:
                file_path = c.get("path", c.get("name", None))
                component_key = c.get("key")

                if file_path and component_key:
                    sonar_files[f"{PROJECT_KEY}:{file_path}"] = component_key

            page += 1
            time.sleep(0.5)

        else:
            print(f"API Error: {response.status_code} - {response.text}")
            break

    return sonar_files



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

sonar_results_all_metrics = {}
for index, row in df_filtered.iterrows():
    component_key = row["sonar_component_key"]
    sonar_results_all_metrics[row["file_path"]] = get_all_sonar_metrics(component_key)

sonar_df_all_metrics = pd.DataFrame.from_dict(sonar_results_all_metrics, orient="index")
sonar_df_all_metrics.reset_index(inplace=True)
sonar_df_all_metrics.rename(columns={"index": "file_path"}, inplace=True)

df_final = df_filtered.merge(sonar_df_all_metrics, on="file_path", how="left")

final_file_path = "github_code_dataset_with_all_sonar_metrics.csv"
df_final.to_csv(final_file_path, index=False)





