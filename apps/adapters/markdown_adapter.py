import os
from typing import List

class MarkdownAdapter:
    @staticmethod
    def read_file(path: str) -> str | None:
        if not os.path.exists(path):
            print(f"info: '{path}' does not exist.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod    
    def write_file(file_path: str, content: str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"info: File '{file_path}' was written.")

    @staticmethod
    def list_markdown_files(folder_path: str) -> List[str]:
        markdown_files = []

        if not os.path.isdir(folder_path):
            print(f"info: Directory '{folder_path}' does not exist or is not a directory.")
            return []

        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isfile(full_path) and entry.lower().endswith('.md'):
                markdown_files.append(entry)

        return markdown_files

    @staticmethod
    def read_canon_directory(folder_path: str, with_thumbnail: bool = False) -> str | None:
        if not os.path.isdir(folder_path):
            print(f"info: Directory '{folder_path}' does not exist or is not a directory.")
            return None

        all_content = []

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".md"):
                    if not with_thumbnail and file_name == "thumbnail.md":
                        continue  # Skip this file
                    
                    file_path = os.path.join(root, file_name)
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        all_content.append(f"### {file_name}\n")
                        all_content.append(f.read())
                        all_content.append("\n\n")

        if not all_content:
            return None
        return "".join(all_content).rstrip()
