import requests
import os
from github import Github
import re
GITHUB_TOKEN = "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"
GITHUB_API_URL = "https://api.github.com/search/repositories"
g = Github(GITHUB_TOKEN)

MAX_FILE_SIZE = 20000
MAX_REPOS = 200
MAX_FILES = 20

os.makedirs("smaller-git-dataset", exist_ok=True)

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

params = {
    "q": "language: python stars:>10",
    "sort": "stars",
    "order": "desc",
    "per_page": 200,
    "page": 1
}



local_import_pattern = re.compile(r"import (\w+)|from (\w+) import")
def is_independent(code, repo_files):
    matches = local_import_pattern.findall(code)
    for match in matches:
        imported_module = match[0] or match[1]
        if f"{imported_module}.py" in repo_files:
            return False
    return True

repositories = []
while len(repositories) < MAX_REPOS and params["page"] <= 3:  # Limit to 200 repos (2 pages)
    response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"⚠️ API Error: {response.status_code}")
        break

    data = response.json()
    repositories.extend(data["items"])  # Add repos to list

    params["page"] += 1  # Go to the next page

# 🔹 Limit to 200 repositories
repositories = repositories[:MAX_REPOS]
print(f"✅ Fetched {len(repositories)} Python repositories.")


# 🔹 Function to fetch Python files from a repository
def fetch_python_files(repo):
    repo_name = repo["full_name"]
    files_url = repo["url"] + "/contents"

    try:
        response = requests.get(files_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ Error fetching files for {repo_name}")
            return

        files = response.json()
        repo_files = {file["name"] for file in files if file["type"] == "file"}
        count = 0  # Limit files per repo

        for file in files:
            if count >= MAX_FILES:
                break  # Stop after 10 files

            if file["type"] == "file" and file["name"].endswith(".py") and file["size"] < MAX_FILE_SIZE:
                file_url = file["download_url"]

                # 🔹 Download and save the file
                response = requests.get(file_url)
                code = response.text
                if is_independent(code, repo_files):
                    with open(f"smaller-git-dataset/{file['name']}", "w", encoding="utf-8") as f:
                        f.write(code)

                    print(f"✅ Saved: {file['name']} ({file['size']} bytes) from {repo_name}")
                    count += 1

    except Exception as e:
        print(f"⚠️ Error processing {repo_name}: {e}")


# 🔹 Process each repository
for i, repo in enumerate(repositories):
    print(f"🔍 Processing {i + 1}/{len(repositories)}: {repo['full_name']}")
    fetch_python_files(repo)

print("✅ Done processing repositories.")