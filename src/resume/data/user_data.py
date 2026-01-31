from typing import Dict, List
import requests

from src.resume import logger

BLOCKED_REPOS = [
    "lyszt",
    "lyszt.github.io",
]

BLOCKED_SCHEMATICS = {
    "_misc",
}

def get_repos(username: str) -> dict[int, dict[str, str]]:
    url = f'https://api.github.com/users/{username}/repos?per_page=100'
    github_repos = requests.get(url).json()
    repos: Dict[int, Dict[str, str]] =\
        {r['id']: {'name': r['name'], 'desc': r['description'], 'url': r['svn_url'], 'lang': r['language']}
         for r in github_repos if not r['fork'] and not r['name'] in BLOCKED_REPOS and not r['name'].endswith(tuple(BLOCKED_SCHEMATICS))}

    return repos


class UserData:
    def __init__(self):
        self.user_info: Dict[int, Dict[str, str]] = get_repos('lyszt')
        skills_set = set()

        # type: List[Dict[str, str]]
        self.core_projects = []
        self.edu_projects = []
        self.legacy_projects = []

        for repo in self.user_info.values():
            name = repo.get('name', '')

            if lang := repo.get("lang"):
                skills_set.add(lang)

            if name.endswith("_core"):
                self.core_projects.append(repo)
            elif name.endswith("_edu"):
                self.edu_projects.append(repo)
            elif name.endswith("_legacy"):
                self.legacy_projects.append(repo)

        self.skills = sorted(list(skills_set))
        logger.info(f"{self.skills, self.core_projects, self.edu_projects, self.legacy_projects}")