from rapidfuzz import fuzz


def keyword_score(resume_text, keywords):
    found_keywords = [kw for kw in keywords if fuzz.partial_ratio(
        kw.lower(), resume_text.lower()) > 70]
    score = int((len(found_keywords) / len(keywords)) * 40) if keywords else 0
    return score, found_keywords
