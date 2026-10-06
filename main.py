#import statements
from pathlib import Path
from analyser import analyse_document
from document_io import read_document, save_analysis_to_json

def parse_keywords(keyword_input: str) -> list[str]:
    keywords = []
    for item in keyword_input.split(","):
        keyword = item.strip()
        if keyword:
            keywords.append(keyword)
    return keywords

def main() -> None:
    project_directory = Path(__file__).parent

    document_name = input("Enter the document name (with extension): ").strip()
    if not document_name:
        print("Document name cannot be empty.")
        return

    keywords_input = input("Enter keywords separated by commas: ")
    keywords = parse_keywords(keywords_input)
    if not keywords:
        print("Keywords cannot be empty.")
        return

    document_path = project_directory / "documents" / document_name
    output_path = project_directory / "documents" /"analysis.txt"

    #keywords = [keyword.strip() for keyword in keywords_input.split(",") if keyword.strip()]    

    try:
        document_text = read_document(document_path)
        analysis = analyse_document(document_text, keywords)
        save_analysis_to_json(analysis, output_path)

        print("\nDocument analysis")
        print(f"Document: {document_name}")
        print(f"Characters: {analysis['character_count']}")
        print(f"Words: {analysis['word_count']}")
        print(f"Keywords searched: {analysis['keyword_count']}")
        print(f"Keywords matched: {analysis['match_count']}")

        matches = ", ".join(analysis["matches"])
        print(f"Matches: {matches or 'No matches'}")

        print(f"\nAnalysis saved to: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()