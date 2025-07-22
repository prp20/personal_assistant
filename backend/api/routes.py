from flask import Blueprint, request, jsonify
from backend.parsers.pdf_parser import parse_pdf
from backend.scoring.keyword_match import keyword_score
from backend.scoring.structure_check import structure_score
from backend.scoring.readability_check import readability_score
from backend.scoring.formatting_check import formatting_score
from backend.llm_suggestions.suggestions_generator import generate_suggestions
from backend.api.models import db, JobApplication

api_blueprint = Blueprint('api', __name__, url_prefix="/api")


@api_blueprint.route("/score", methods=["POST"])
def score_resume():
    data = request.json
    resume_text = data.get("resume_text")
    jd_text = data.get("jd_text")

    k_score = keyword_score(resume_text, jd_text)
    structure_score_result = structure_score(resume_text)
    readability_result, readability_metric = readability_score(resume_text)
    formatting_result = formatting_score(resume_text)

    return jsonify({
        "keyword_score": k_score,
        "structure_score": structure_score_result,
        "readability_score": readability_result,
        "readability_metric": readability_metric,
        "formatting_score": formatting_result
    })


@api_blueprint.route("/suggestions", methods=["POST"])
def suggestions():
    data = request.json
    resume_text = data.get("resume_text")
    jd_text = data.get("jd_text")

    suggestions = generate_suggestions(jd_text, resume_text)
    return jsonify({"suggestions": suggestions})


@api_blueprint.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = JobApplication.query.all()
    result = [
        {
            "id": job.id,
            "Company": job.company,
            "Role": job.role,
            "Location": job.location,
            "Status": job.status,
            "Application URL": job.application_url,
            "Notes": job.notes,
        }
        for job in jobs
    ]
    return jsonify(result)


@api_blueprint.route("/jobs", methods=["POST"])
def add_or_update_job():
    data = request.json
    if "id" in data:
        job = JobApplication.query.get(data["id"])
        if job:
            job.company = data["Company"]
            job.role = data["Role"]
            job.location = data["Location"]
            job.status = data["Status"]
            job.application_url = data["Application URL"]
            job.notes = data["Notes"]
    else:
        job = JobApplication(
            company=data["Company"],
            role=data["Role"],
            location=data["Location"],
            status=data["Status"],
            application_url=data["Application URL"],
            notes=data["Notes"],
        )
        db.session.add(job)

    db.session.commit()
    return jsonify({"message": "Success"})


@api_blueprint.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = JobApplication.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
    return jsonify({"message": "Deleted"})
