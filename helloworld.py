from pathlib import Path
from time import perf_counter

start_time = perf_counter()
document_path = Path(__file__).parent / "documents"

def read_document(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()

def write_document(file_path: Path, content: str) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        file.write(content)

def helloworld():
    print("Hello, World!")
    


elapsed_time = perf_counter() - start_time
if __name__ == "__main__":
    helloworld()
    print(f"Elapsed time: {elapsed_time} seconds")