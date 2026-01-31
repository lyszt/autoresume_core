from typing import Dict, List
import requests

from src.resume import logger

BLOCKED_REPOS = [
    "lyszt",
]

def get_repos(username: str) -> List[Dict[str, str]]:

    github_repos = requests.get(f'https://api.github.com/users/{username}/repos').json()
    repos: Dict[int, Dict[str, str]] =\
        {r['id']: {'name': r['name'], 'desc': r['description'], 'url': r['homepage'], 'lang': r['language']}
         for r in github_repos if not r['fork'] and not r['name'] in BLOCKED_REPOS }

    logger.info(repos)
    return github_repos.json()


class UserData:
    def __init__(self):
        # Repository dictionary - Holds NAME, DESCRIPTION, LANGUAGE, URL
        self.repos: Dict[int, Dict[str, str]]= {}
        get_repos(username="lyszt")


