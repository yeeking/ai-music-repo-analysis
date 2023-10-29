from datetime import datetime
import requests
import pandas as pd
import time 
TOKEN = "YOUR_GITHUB_ACCESS_TOKEN"  # Replace this with your GitHub Personal Access Token
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

BASE_URL = "https://api.github.com/repos/"

def get_repo_age(user_repo):
    repo_info_url = BASE_URL + user_repo
    response = requests.get(repo_info_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to fetch details for {user_repo}. Status code: {response.status_code}")
        return None

    data = response.json()
    creation_date_str = data['created_at']
    creation_date = datetime.strptime(creation_date_str, '%Y-%m-%dT%H:%M:%SZ')
    
    current_date = datetime.utcnow()
    age = current_date - creation_date

    return age.days


def get_repo_details(url):
    user_repo = url.split("github.com/")[-1]
    repo_info_url = BASE_URL + user_repo

    response = requests.get(repo_info_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch details for {url}. Status code: {response.status_code}")
        return None

    data = response.json()
    stars = data['stargazers_count']
    forks = data['forks_count']
    watchers = data['subscribers_count']
    issues = data['open_issues_count']
    network_count = data['network_count']

    # Fetching download counts across all releases
    release_url = BASE_URL + user_repo + "/releases"
    releases = requests.get(release_url, headers=HEADERS).json()
    download_count = sum([asset['download_count'] for release in releases for asset in release['assets']])

    # Fetching commit count
    commits_url = BASE_URL + user_repo + "/commits"
    commits_response = requests.get(commits_url, headers=HEADERS)
    commits_count = len(commits_response.json())

    # Fetching languages
    lang_url = BASE_URL + user_repo + "/languages"
    lang = requests.get(lang_url, headers=HEADERS)
    lang_list = [k for k in lang.json().keys()]
    
    age = get_repo_age(user_repo=user_repo)

    return {
        "Repository": user_repo,
        "Stars": stars,
        "Forks": forks,
        "Downloads": download_count,
        "Watchers": watchers,
        "Open Issues": issues,
        "Network Count": network_count,
        "Commit Count": commits_count, 
        "Age (days)":age, 
        "Languages" : lang_list
    }

def main():
    # url_data = pd.read_csv('../data/raw-repo-list.csv')
    url_data = pd.read_csv('../data/404s-fixed2.csv')

    details_list = []

    # for repo in repos:
    for ind,row in url_data.iterrows():
        repo = row["Github repository"]
        print(repo)
        details = get_repo_details(repo)
        if details:
            details_list.append(details)
        # break
        time.sleep(0.5)

    # Create dataframe and save to CSV
    df = pd.DataFrame(details_list)
    df.to_csv("github_stats.csv", index=False)

    print("Data saved to github_stats.csv")

if __name__ == "__main__":
    main()

