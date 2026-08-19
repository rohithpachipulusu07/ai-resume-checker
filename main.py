import os
import sys

# Add backend directory to sys.path so modules can be imported directly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "AI-Resume-Analyzer", "backend")

if os.path.exists(backend_dir):
    sys.path.append(backend_dir)
else:
    sys.path.append(os.path.join(current_dir, "backend"))

from main import app
