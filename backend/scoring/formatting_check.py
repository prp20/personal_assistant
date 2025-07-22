def formatting_score(resume_text):
    bad_patterns = ['table', 'column', 'graphic']
    score = 20 if not any(bad in resume_text.lower()
                          for bad in bad_patterns) else 10
    return score, bad_patterns
