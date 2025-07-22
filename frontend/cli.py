import argparse
from parsers.pdf_parser import parse_pdf
# from parsers.docx_parser import parse_docx
from scoring.keyword_match import keyword_score
from scoring.structure_check import structure_score
from scoring.readability_check import readability_score
from scoring.formatting_check import formatting_score
from suggestions.suggestions_generator import generate_suggestions


def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file format.")


def main():
    parser = argparse.ArgumentParser(description="ATS Resume Scorer")
    parser.add_argument("--resume", required=True,
                        help="Path to resume file (.pdf or .docx)")
    parser.add_argument("--jd", required=True,
                        help="Path to job description text file")
    args = parser.parse_args()

    resume_text = parse_resume(args.resume)
    jd_text = open(args.jd, "r", encoding="utf-8").read()

    keywords = jd_text.lower().split()[:20]  # Naive keyword extraction for MVP

    k_score, found_keywords = keyword_score(resume_text, keywords)
    s_score, found_sections = structure_score(resume_text)
    r_score, readability_metric = readability_score(resume_text)
    f_score, _ = formatting_score(resume_text)

    total_score = k_score + s_score + r_score + f_score

    suggestions = generate_suggestions(jd_text, resume_text)

    print(f"\n=== ATS Score Breakdown ===")
    print(f"Keywords Match: {k_score}/40  | Found: {found_keywords}")
    print(f"Structure: {s_score}/20       | Found: {found_sections}")
    print(
        f"Readability: {r_score}/20     | Flesch Reading Ease: {readability_metric}")
    print(f"Formatting: {f_score}/20      | Simplicity Check Passed\n")
    print(f"Total ATS Score: {total_score}/100")

    print("\n=== Suggestions from LLM ===")
    print(suggestions)


if __name__ == "__main__":
    main()
