import os
import sys
import tempfile
import unittest

# Ensure parent and current directory are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from backend.resume_parser import extract_text_from_file, extract_resume_sections
    from backend.skill_extractor import extract_skills, generate_ats_suggestions
    from backend.matcher import calculate_match_breakdown
    from backend.data_generator import generate_random_resume, generate_random_job_description, generate_training_dataset
    from backend.model_trainer import train_model
except ImportError:
    from resume_parser import extract_text_from_file, extract_resume_sections
    from skill_extractor import extract_skills, generate_ats_suggestions
    from matcher import calculate_match_breakdown
    from data_generator import generate_random_resume, generate_random_job_description, generate_training_dataset
    from model_trainer import train_model


class ResumeAnalyzerTests(unittest.TestCase):
    def test_extract_text_from_txt_file(self):
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
            f.write('Python developer with SQL, Flask, and machine learning skills.')
            temp_path = f.name

        try:
            text = extract_text_from_file(temp_path)
            self.assertIn('Python', text)
            self.assertIn('Flask', text)
        finally:
            os.unlink(temp_path)

    def test_extract_skills_returns_common_keywords(self):
        text = 'Experienced Python developer with SQL, AWS, Docker, and REST APIs.'
        skills = extract_skills(text)
        self.assertIn('python', skills)
        self.assertIn('sql', skills)
        self.assertIn('docker', skills)

    def test_match_resume_to_job_returns_breakdown(self):
        resume = 'Python, SQL, Docker, REST APIs, AWS, Agile'
        job = 'Looking for Python developer with SQL and REST API experience, Docker, AWS'
        result = calculate_match_breakdown(resume, job)

        self.assertIn('overall_match', result)
        self.assertIn('keyword_match', result)
        self.assertIn('semantic_match', result)
        self.assertIn('skill_match', result)
        self.assertGreaterEqual(result['overall_match'], 70)
        self.assertLessEqual(result['overall_match'], 100)

    def test_extract_resume_sections_detects_experience(self):
        resume = '''
        Contact Information
        john@example.com | +1 (555) 123-4567

        Education
        B.Tech in Computer Science

        Skills
        Python, SQL, FastAPI

        Experience
        Software Engineer at ABC Corp
        - Built APIs and data pipelines

        Projects
        Resume Analyzer project

        Certifications
        AWS Certified Developer
        '''

        sections = extract_resume_sections(resume)
        self.assertTrue(sections['contact_information'])
        self.assertTrue(sections['education'])
        self.assertTrue(sections['skills'])
        self.assertTrue(sections['projects'])
        self.assertTrue(sections['certifications'])
        self.assertTrue(sections['experience'])

    def test_generate_ats_suggestions_reports_key_issues(self):
        resume = '''
        Skills
        SQL, AWS, Docker

        Projects
        Built a dashboard
        '''

        suggestions = generate_ats_suggestions(resume)
        self.assertTrue(any('Python' in suggestion for suggestion in suggestions))
        self.assertTrue(any('Experience' in suggestion for suggestion in suggestions))
        self.assertTrue(any('Skills' in suggestion for suggestion in suggestions))
        self.assertTrue(any('measurable results' in suggestion.lower() for suggestion in suggestions))

    def test_generate_random_resume_produces_valid_text(self):
        resume = generate_random_resume()
        self.assertIsInstance(resume, str)
        self.assertIn('Contact Information', resume)
        self.assertIn('Education', resume)
        self.assertIn('Skills', resume)
        self.assertIn('Experience', resume)

    def test_generate_random_job_description_produces_valid_text(self):
        job = generate_random_job_description()
        self.assertIsInstance(job, str)
        self.assertIn('Position:', job)
        self.assertIn('Company:', job)
        self.assertIn('Requirements:', job)

    def test_generate_training_dataset_produces_samples(self):
        dataset = generate_training_dataset(num_samples=10)
        self.assertEqual(len(dataset), 10)
        for item in dataset:
            self.assertIn('resume', item)
            self.assertIn('job_description', item)
            self.assertIn('score', item)
            self.assertGreaterEqual(item['score'], 0)
            self.assertLessEqual(item['score'], 1)

    def test_model_training_completes_successfully(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            model, vectorizer = train_model(num_samples=50)
            self.assertIsNotNone(model)
            self.assertIsNotNone(vectorizer)


if __name__ == '__main__':
    unittest.main()
