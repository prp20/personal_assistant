import os
from groq import Groq
from dotenv import load_dotenv

# Load API Key from .env file or environment variable
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_suggestions(job_description: str, resume: str) -> str:
    prompt = f"""
    You are an expert ATS resume reviewer.

    Given the following:
    ---
    Job Description:
    {job_description}

    Resume:
    {resume}
    ---

    Provide:
    1. A summary of how well the resume matches the JD.
    2. Specific suggestions to improve the resume for ATS (e.g., missing keywords, formatting tips).
    3. Rate the match out of 10.

    Be brief and actionable. Provide your output formatted as Markdown, with clear headings, bullet points, and numbered lists.
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Groq supports LLaMA3 models
            messages=[
                {"role": "system", "content": "You are an ATS resume optimization expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating suggestions: {e}"
