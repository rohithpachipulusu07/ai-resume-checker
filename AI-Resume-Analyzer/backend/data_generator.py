import random

FIRST_NAMES = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Jessica", "Robert", "Jennifer"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

COMPANIES = ["Tech Corp", "Data Inc", "Cloud Solutions", "AI Systems", "Software House", "Digital Labs", "Innovation Co", "Future Tech"]
JOB_TITLES = ["Software Engineer", "Data Scientist", "Full Stack Developer", "Backend Developer", "DevOps Engineer", "ML Engineer", "Frontend Developer"]
RESPONSIBILITIES = [
    "Developed REST APIs", "Built machine learning models", "Managed cloud infrastructure",
    "Designed databases", "Optimized performance", "Led team projects", "Wrote automated tests",
    "Deployed applications", "Analyzed data", "Mentored junior developers"
]

SKILL_SETS = [
    ["Python", "SQL", "Flask", "AWS"],
    ["JavaScript", "React", "Node.js", "MongoDB"],
    ["Java", "Spring Boot", "Docker", "Kubernetes"],
    ["Python", "TensorFlow", "PyTorch", "Pandas"],
    ["C++", "Linux", "Git", "CMake"],
    ["Go", "Docker", "AWS", "Microservices"],
    ["Python", "Django", "PostgreSQL", "Redis"],
    ["TypeScript", "Angular", "REST API", "HTML/CSS"],
]

CERTIFICATIONS = [
    "AWS Certified Developer", "Google Cloud Professional", "Azure Administrator",
    "Kubernetes Certified", "Linux Foundation Certified", "Oracle Certified Associate"
]

EDUCATION_LEVELS = ["B.Tech", "Bachelor", "Master", "MBA", "B.Sc", "M.Sc"]
UNIVERSITIES = ["State University", "Tech Institute", "Engineering College", "University of Science"]

def generate_random_resume():
    """Generate a random resume text."""
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    email = f"{name.lower().replace(' ', '.')}@email.com"
    phone = f"+1 ({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    contact = f"""Contact Information
{name}
{email}
{phone}
"""
    
    education = f"""Education
{random.choice(EDUCATION_LEVELS)} in Computer Science
{random.choice(UNIVERSITIES)}
"""
    
    skills = random.sample(SKILL_SETS, k=random.randint(1, 3))
    skills_flat = ", ".join([s for skill_set in skills for s in skill_set])
    skills_section = f"""Skills
{skills_flat}
"""
    
    experience = f"""Experience
"""
    for _ in range(random.randint(1, 3)):
        company = random.choice(COMPANIES)
        title = random.choice(JOB_TITLES)
        years = random.randint(1, 5)
        experience += f"{title} at {company} ({years} years)\n"
        for _ in range(random.randint(1, 3)):
            experience += f"- {random.choice(RESPONSIBILITIES)}\n"
    
    projects = """Projects
"""
    for _ in range(random.randint(1, 2)):
        project_skills = ", ".join(random.sample(skills_flat.split(", "), k=min(2, len(skills_flat.split(", ")))))
        projects += f"Project built with {project_skills}\n"
    
    certifications = f"""Certifications
{random.choice(CERTIFICATIONS)}
"""
    
    return contact + education + skills_section + experience + projects + certifications

def generate_random_job_description():
    """Generate a random job description text."""
    title = random.choice(JOB_TITLES)
    company = random.choice(COMPANIES)
    
    job_desc = f"""Position: {title}
Company: {company}

About the Role:
We are looking for a talented professional to join our team.

Requirements:
"""
    
    required_skills = random.sample(SKILL_SETS, k=random.randint(1, 3))
    for skill_set in required_skills:
        for skill in skill_set:
            job_desc += f"- {skill}\n"
    
    job_desc += f"""
Responsibilities:
"""
    for _ in range(random.randint(2, 4)):
        job_desc += f"- {random.choice(RESPONSIBILITIES)}\n"
    
    job_desc += f"""
Experience Required:
- {random.randint(1, 5)} years of professional experience
- Strong problem-solving skills
- Experience with {random.choice(['Cloud platforms', 'Databases', 'DevOps', 'Microservices'])}
"""
    
    return job_desc

def generate_training_dataset(num_samples=500):
    """Generate a training dataset of resume-job description pairs with labels."""
    dataset = []
    
    for _ in range(num_samples):
        resume = generate_random_resume()
        job = generate_random_job_description()
        
        resume_skills = set(skill.lower() for skill_set in random.sample(SKILL_SETS, k=random.randint(1, 3)) for skill in skill_set)
        job_skills = set(skill.lower() for skill_set in random.sample(SKILL_SETS, k=random.randint(1, 3)) for skill in skill_set)
        
        overlap = len(resume_skills.intersection(job_skills))
        total = max(len(job_skills), 1)
        match_score = min(100, (overlap / total * 100) + random.randint(-10, 10))
        match_score = max(0, match_score)
        
        dataset.append({
            'resume': resume,
            'job_description': job,
            'score': match_score / 100
        })
    
    return dataset
