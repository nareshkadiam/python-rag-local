import json
from pathlib import Path

def read_document(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()

def save_analysis_to_json(analysis: dict, output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=2)