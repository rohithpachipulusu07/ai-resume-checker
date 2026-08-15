# Quick Start Guide - AI Resume Analyzer

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Upload Directory
```bash
mkdir uploads
```

### Step 3: Train the ML Model (Optional but Recommended)
This trains a machine learning model on 500 synthetic resume-job description pairs for improved accuracy.

```bash
cd backend
python train_model_cli.py --samples 500
```

Expected output:
```
============================================================
Resume Matching Model Training
============================================================

Generating 500 training samples...
Vectorizing text data...
Training model...
Saving model to .../trained_model.pkl
Training complete!
```

### Step 4: Start the API Server
```bash
cd backend
uvicorn main:app --reload
```

The API server runs at: `http://localhost:8000`

### Step 5: Open the Web Interface
```bash
# Open in your default browser
start ../frontend/index.html

# Or manually navigate to the file in your browser
```

## Using the Analyzer

1. **Upload a resume** - Click the file input and select a PDF, DOCX, or TXT file
2. **Paste a job description** - Copy and paste the job posting text
3. **Click "Analyze"** - Get instant matching scores and recommendations

## Expected Results

The analyzer provides:
- **Overall Match %** - Combined score from all metrics
- **Keyword Match %** - Skill overlap with job requirements
- **Semantic Match %** - Text similarity analysis
- **Skill Match %** - Required skills found in resume
- **Missing Skills** - Technologies needed but not listed
- **ATS Suggestions** - 4-5 actionable improvements
- **Interview Questions** - Generated questions based on resume

## Example

**Resume:** Software Engineer with Python, Django, PostgreSQL, AWS experience

**Job Description:** Senior Python Developer - Python, Django, PostgreSQL, Redis, Kubernetes, Docker

**Results:**
- Overall Match: 78.5%
- Keyword Match: 82.3%
- Semantic Match: 75.1%
- Skill Match: 80.0%
- Missing Skills: Redis, Kubernetes, Docker
- ATS Suggestions:
  - ✓ Strong Python and Django skills
  - ✓ Database experience matches
  - ⚠ Missing container/orchestration skills
  - ✓ Clear experience section

## Testing

Run the test suite to verify everything works:

```bash
cd backend
python -m unittest test_resume_analyzer -v
```

Should see: `Ran 9 tests in X.XXXs - OK`

## API Usage

### Analyze Resume
```bash
curl -X POST http://localhost:8000/analyze \
  -F "resume=@resume.pdf" \
  -F "job_description=<job_description.txt" \
  -F "use_trained_model=true"
```

### Train Model
```bash
curl -X POST "http://localhost:8000/train?num_samples=500"
```

## Troubleshooting

**API won't start:**
- Check if port 8000 is already in use
- Try: `uvicorn main:app --reload --port 8001`

**File upload fails:**
- Ensure `uploads/` directory exists
- Check file format (PDF, DOCX, TXT only)

**Weak matching results:**
- Ensure resume contains actual job requirements as text
- Check for typos in technology names
- Train the model for better accuracy: `python train_model_cli.py --samples 1000`

## Architecture Overview

```
Browser (Frontend)
    ↓ HTTP/FormData
FastAPI Server (Backend)
    ├── Resume Parser (Extract text + sections)
    ├── Skill Extractor (Find tech keywords)
    ├── Heuristic Matcher (Calculate scores)
    ├── ML Model (RandomForestRegressor - optional)
    └── ATS Generator (Improvement suggestions)
    ↓ JSON
Browser (Results)
```

## Next Steps

After the basic setup works:

1. **Customize skill keywords** - Edit `backend/skill_extractor.py` SKILLS list
2. **Improve ML accuracy** - Train with more samples: `python train_model_cli.py --samples 2000`
3. **Integrate with job boards** - Use the API in your own applications
4. **Deploy to cloud** - Host on AWS Lambda, Heroku, or Azure Functions

## Supporthttp://localhost:8000

- Check [README.md](../README.md) for detailed documentation
- Review test cases in [test_resume_analyzer.py](backend/test_resume_analyzer.py) for usage examples
- Check source code comments for implementation details
