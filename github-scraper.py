import requests
import os
from github import Github
import re
from concurrent.futures import ThreadPoolExecutor
import csv
GITHUB_TOKEN = "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"
GITHUB_API_URL = "https://api.github.com/search/repositories"
g = Github(GITHUB_TOKEN)

MAX_FILE_SIZE = 30000
MIN_FILE_SIZE = 15000
MAX_REPOS = 200
MAX_FILES = 20
THREADS = 10

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# 🔹 Query to fetch Python repositories (Sorted by Stars)
params = {
    "q": "language:python stars:>10",
    "sort": "stars",
    "order": "desc",
    "per_page": 100,  # Max 100 per request
    "page": 1
}

# 🔹 Regex pattern to check for local imports
local_import_pattern = re.compile(r"import (\w+)|from (\w+) import")


def is_independent(code, repo_files):
    """Check if a script has local imports that might cause dependency issues."""
    matches = local_import_pattern.findall(code)
    for match in matches:
        imported_module = match[0] or match[1]
        if f"{imported_module}.py" in repo_files:
            return False
    return True


# 🔹 Create directories
os.makedirs("messy_python_files", exist_ok=True)

# 🔹 Initialize CSV File
csv_file = "messy_python_dataset.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["repo_name", "file_name", "file_size", "file_url", "full_code"])


def fetch_python_files(repo):
    """Fetch Python files from a repository, save them, and store in CSV."""
    repo_name = repo["full_name"].replace("/", "_")  # Avoid slashes in file names
    files_url = repo["url"] + "/contents"

    try:
        response = requests.get(files_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ Error fetching files for {repo_name}")
            return

        files = response.json()
        repo_files = {file["name"] for file in files if file["type"] == "file"}
        count = 0  # Limit files per repo

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            for file in files:
                if count >= MAX_FILES:
                    break  # Stop after reaching max files per repo

                if file["type"] == "file" and file["name"].endswith(".py") and file["size"] < MAX_FILE_SIZE and file["size"] > MIN_FILE_SIZE:
                    file_url = file["download_url"]

                    # 🔹 Download the file
                    response = requests.get(file_url)
                    code = response.text

                    # 🔹 Ensure it's independent before saving
                    if is_independent(code, repo_files):
                        file_name = f"{repo_name}_{file['name']}"
                        file_path = os.path.join("messy_python_files", file_name)

                        # 🔹 Save file locally for GitHub commit
                        with open(file_path, "w", encoding="utf-8") as f_py:
                            f_py.write(code)

                        # 🔹 Append to CSV
                        writer.writerow([repo_name, file_name, file["size"], file_url, code])

                        print(f"✅ Saved: {file_name} ({file['size']} bytes) from {repo_name}")
                        count += 1

    except Exception as e:
        print(f"⚠️ Error processing {repo_name}: {e}")


# 🔹 Fetch repositories
repositories = []
while len(repositories) < MAX_REPOS and params["page"] <= 3:
    response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"⚠️ API Error: {response.status_code}, Message: {response.text}")
        break

    data = response.json()
    repositories.extend(data["items"])  # Add repos to list

    params["page"] += 1  # Next page

# 🔹 Limit to MAX_REPOS
repositories = repositories[:MAX_REPOS]
print(f"✅ Fetched {len(repositories)} Python repositories.")

# 🔹 Multi-threaded execution for faster downloads
with ThreadPoolExecutor(max_workers=THREADS) as executor:
    executor.map(fetch_python_files, repositories)

print("✅ Done processing repositories.")