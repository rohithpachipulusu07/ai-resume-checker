SKILLS = [
    "python",
    "c",
    "java",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "nlp",
    "sql",
    "mysql",
    "git",
    "github",
    "docker",
    "aws",
    "gcp",
    "html",
    "css",
    "javascript",
    "fastapi",
    "flask"
]

PYTHON_KEYWORDS = [
    'python', 'python3', 'py', 'django', 'flask', 'fastapi',
    'pandas', 'numpy', 'requests', 'json', 'api', 'automation'
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def generate_ats_suggestions(text):
    suggestions = []
    cleaned = (text or '').lower()

    if not any(keyword in cleaned for keyword in PYTHON_KEYWORDS):
        suggestions.append('⚠ Add more keywords related to Python.')

    if 'experience' not in cleaned and 'work experience' not in cleaned and 'professional experience' not in cleaned:
        suggestions.append("⚠ Your resume doesn't contain an Experience section.")

    if 'skills' in cleaned or 'technical skills' in cleaned:
        suggestions.append('✓ Your Skills section is clearly identifiable.')

    if 'project' not in cleaned and 'projects' not in cleaned:
        suggestions.append('⚠ Consider adding measurable results to your projects.')
    elif any(word in cleaned for word in ['built', 'developed', 'created', 'improved']) and not any(word in cleaned for word in ['increased', 'reduced', 'optimized', 'improved by', 'delivered', 'achieved']):
        suggestions.append('⚠ Consider adding measurable results to your projects.')

    return suggestions


def generate_interview_questions(text):
    detected = extract_skills(text)
    questions = []
    lower_text = (text or '').lower()

    if 'python' in detected or 'python' in lower_text:
        questions.append('1. What is overfitting?')
        questions.append('2. Explain precision and recall.')

    if 'machine learning' in detected or 'machine learning' in lower_text:
        questions.append('3. What is the difference between supervised and unsupervised learning?')

    if 'nlp' in detected or 'nlp' in lower_text:
        questions.append('4. What is tokenization in NLP?')

    if 'tensorflow' in detected or 'tensorflow' in lower_text:
        questions.append('5. What is the difference between TensorFlow and PyTorch?')

    if not questions:
        questions.append('1. Tell me about a project you have worked on recently.')

    return questions
