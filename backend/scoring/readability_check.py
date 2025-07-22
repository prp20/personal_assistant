import spacy
import textdescriptives

nlp = spacy.load("en_core_web_md")
nlp.add_pipe("textdescriptives/readability")


def readability_score(resume_text):
    doc = nlp(resume_text)
    flesch = doc._.readability["flesch_reading_ease"]
    score = min(max(int(flesch / 5), 0), 20)
    return score, flesch
