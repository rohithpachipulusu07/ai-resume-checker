import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

try:
    from .data_generator import generate_training_dataset
except ImportError:  # pragma: no cover
    from data_generator import generate_training_dataset

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'trained_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

def train_model(num_samples=500):
    """Train a machine learning model on random resume-job description pairs."""
    print(f"Generating {num_samples} training samples...")
    dataset = generate_training_dataset(num_samples)
    
    resumes = [item['resume'] for item in dataset]
    jobs = [item['job_description'] for item in dataset]
    scores = [item['score'] for item in dataset]
    
    combined_texts = [f"{resume}\n{job}" for resume, job in zip(resumes, jobs)]
    
    print("Vectorizing text data...")
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    X = vectorizer.fit_transform(combined_texts)
    
    print("Training model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, scores)
    
    print(f"Saving model to {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    
    print("Training complete!")
    return model, vectorizer

def load_model():
    """Load the pre-trained model and vectorizer."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("Model not found. Training new model...")
        return train_model()
    
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def predict_match_score(resume, job_description):
    """Use the trained model to predict a match score."""
    try:
        model, vectorizer = load_model()
        combined = f"{resume}\n{job_description}"
        X = vectorizer.transform([combined])
        score = model.predict(X)[0]
        return min(100, max(0, score * 100))
    except Exception as e:
        print(f"Error in model prediction: {e}")
        return None

if __name__ == '__main__':
    train_model(num_samples=500)
