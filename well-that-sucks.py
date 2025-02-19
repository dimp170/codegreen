import requests
import os
from github import Github, GithubException
import time


GITHUB_TOKEN = "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"
g = Github(GITHUB_TOKEN)


query = "language:Python stars:>1000 size:>10000"
repo_list = g.search_repositories(query=query)


DATASET_DIR = "complex_python_dataset"
os.makedirs(DATASET_DIR, exist_ok=True)


def download_large_python_files(repo):

    try:
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)


            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
                continue


            if file_content.path.endswith(".py") and file_content.size > 10000:
                file_url = file_content.download_url
                response = requests.get(file_url)
                if response.status_code == 200:
                    file_path = os.path.join(DATASET_DIR, file_content.name)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"Downloaded: {file_content.name} ({file_content.size} bytes)")

    except GithubException as e:
        print(f"GitHub API Error for {repo.full_name}: {e}")
        time.sleep(5)  # Avoid rate limit issues

    except Exception as e:
        print(f"Error fetching files from {repo.full_name}: {e}")


# ✅ Fetch files from top repositories
repo_count = 0
for repo in repo_list[:10]:  # Limit to 10 repositories
    print(f"Searching {repo.full_name}...")
    download_large_python_files(repo)
    repo_count += 1

    # ✅ Handle API Rate Limit (Avoid hitting GitHub's request limit)
    if repo_count % 5 == 0:
        print("Waiting to avoid GitHub rate limits...")
        time.sleep(10)

print("Dataset collection complete! Complex Python scripts are stored in 'complex_python_dataset'.")