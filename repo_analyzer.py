import requests
from dataclasses import dataclass

@dataclass
class Repository:
    name: str
    language: str
    stars: int
    forks: int
    is_fork: bool

def parse_repo_list(repos):
    repo_list = []
    for repo in repos:
        repo_list.append(Repository(repo["name"], repo["language"], repo["stargazers_count"], repo["forks_count"], repo["fork"]))
    for repo in repo_list:
        print(repo)

def get_repos_for_user(username):
    url = f"https://api.github.com/users/{username}/repos"
    print("Fetching repos for user:", username)
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        parse_repo_list(response.json())
    else:
        response.raise_for_status()

def main():
    username = input("Enter GitHub username: ")
    get_repos_for_user(username)

if __name__ == "__main__":
    main()