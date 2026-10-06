def count_words(text: str) -> int:
    words = text.split()
    return len(words)

def count_tags(tags: list[str]) -> int:
    return len(tags)

def contains_keyword(text: str, keyword: str) -> bool:
    cleaned_keyword = keyword.strip()
    if not cleaned_keyword:
        return False
    return cleaned_keyword.lower() in text.lower()

def find_matching_keywords(text: str, keywords: list[str]) -> list[str]:
    matching_keywords = []
    for keyword in keywords:
        if contains_keyword(text, keyword):
            matching_keywords.append(keyword)
    return matching_keywords

def analyse_document(text: str, keywords: list[str]) -> dict:
    matches = find_matching_keywords(text, keywords)
    analysis = {
        "character_count": len(text),
        "word_count": count_words(text),
        "keyword_count": len(keywords),
        "matches": matches,
        "match_count": len(matches)
    }
    return analysis