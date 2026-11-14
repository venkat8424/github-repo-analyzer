import requests
from dataclasses import dataclass

@dataclass
class Repository:
    name: str
    language: str
    stars: int
    forks: int
    is_fork: bool

    def __repr__(self):
        return f"{self.name}\nLanguage: {self.language}\nStars: {self.stars}\nForks: {self.forks}"

def analyze_repos(username, repos):
    original_repos = []
    total_repo_count, original_repo_count, forked_repo_count = 0, 0, 0
    total_stars, max_stars, avg_stars = 0, 0, 0
    lang_map = {}
    repo_with_max_stars = None
    for repo in repos:
        if repo.is_fork:
            forked_repo_count += 1
        else:
            lang = repo.language
            if lang is None:
                lang = "Unknown"
            if lang in lang_map:
                lang_map[lang] = lang_map[lang] + 1
            else:
                lang_map[lang] = 1
            total_stars += repo.stars
            if repo.stars >= max_stars:
                max_stars = repo.stars
                repo_with_max_stars = repo
            original_repo_count += 1
            original_repos.append(repo)
        total_repo_count += 1
    if original_repo_count > 0:
        avg_stars = total_stars / original_repo_count

    original_repos.sort(key=lambda r: r.stars, reverse=True)

    print("GitHub Repository Report")
    print("------------------------")
    print("")
    print("User:", username)
    print("")
    print("Repository Summary")
    print("------------------------")
    print("Public repositories:", total_repo_count)
    print("Original repositories:", original_repo_count)
    print("Forked repositories:", forked_repo_count)
    print("Total stars:", total_stars)
    print("Average stars:", avg_stars)
    if repo_with_max_stars is not None:
        print(f"Most starred: {repo_with_max_stars.name} ({max_stars} stars)")
    print("")
    print("Top Repositories")
    print("------------------------")
    top_five_repos = original_repos[:5]
    for index, top_repo in enumerate(top_five_repos):
        print(f"#{index+1}")
        print(top_repo)
        print("")
    print("")
    print("Languages")
    print("------------------------")
    for lang in lang_map:
        print(f"{lang}: {lang_map[lang]}")

def parse_repo_list(username, repos):
    if len(repos) == 0:
        print(f"No public repositories found for user: {username}")
        return []
    
    repo_list = []
    for repo in repos:
        repo_object = Repository(repo["name"], repo["language"], repo["stargazers_count"], repo["forks_count"], repo["fork"])
        repo_list.append(repo_object)

    return repo_list

def handle_error(status_code):
    if status_code == 404:
        print("GitHub username does not exist")
    elif 500 <= status_code <= 599:
        print("Internal server error")
    else:
        print("Failed to fetch repos for the user")

def get_repos_for_user(username):
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            repos = parse_repo_list(username, response.json())
            if len(repos) > 0:
                analyze_repos(username, repos)
        else:
            handle_error(response.status_code)
    except requests.RequestException:
        print("Encountered a network error")

def main():
    username = input("Enter GitHub username: ")
    get_repos_for_user(username)

if __name__ == "__main__":
    main()