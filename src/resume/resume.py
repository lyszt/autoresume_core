from pathlib import Path

from src.resume.data.user_data import UserData
from src.resume.generator.readme_generator import generate_readme_md


class Main:
    def __init__(self):
        user_data: UserData = UserData()
        output_path = Path(__file__).resolve().parent.parent.parent / "out" / "readme.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        generate_readme_md(user_data, output_path)