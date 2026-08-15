from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from .skill_extractor import extract_skills
except ImportError:  # pragma: no cover
    from skill_extractor import extract_skills

try:
    from .model_trainer import predict_match_score as ml_predict_score
except ImportError:  # pragma: no cover
    try:
        from model_trainer import predict_match_score as ml_predict_score
    except ImportError:  # pragma: no cover
        ml_predict_score = None


def _clamp_percentage(value):
    return max(0, min(round(float(value), 2), 100))


def calculate_match_breakdown(resume_text, job_description, use_trained_model=False):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    if resume_skills or job_skills:
        skill_overlap = resume_skills.intersection(job_skills)
        skill_match = 100 if not job_skills else _clamp_percentage((len(skill_overlap) / len(job_skills)) * 100)
    else:
        skill_match = 0

    keyword_match = 100 if not job_description else _clamp_percentage((len(resume_skills.intersection(job_skills)) / max(len(job_skills), 1)) * 100)

    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    semantic_match = cosine_similarity(vectors[0], vectors[1])[0][0]
    semantic_match = _clamp_percentage(semantic_match * 100)

    heuristic_score = _clamp_percentage((keyword_match * 0.35) + (semantic_match * 0.35) + (skill_match * 0.30))

    if use_trained_model and ml_predict_score:
        try:
            ml_score = ml_predict_score(resume_text, job_description)
            if ml_score is not None:
                overall_match = _clamp_percentage((heuristic_score * 0.4) + (ml_score * 0.6))
            else:
                overall_match = heuristic_score
        except Exception:
            overall_match = heuristic_score
    else:
        overall_match = heuristic_score

    return {
        'overall_match': overall_match,
        'keyword_match': keyword_match,
        'semantic_match': semantic_match,
        'skill_match': skill_match,
    }


def calculate_match_score(resume_text, job_description, use_trained_model=False):
    return calculate_match_breakdown(resume_text, job_description, use_trained_model)['overall_match']
