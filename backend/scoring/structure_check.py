def structure_score(resume_text):
    required_sections = ["experience", "education", "skills", "projects"]
    found_sections = [
        sec for sec in required_sections if sec.lower() in resume_text.lower()]
    score = int((len(found_sections) / len(required_sections)) * 20)
    return score, found_sections
