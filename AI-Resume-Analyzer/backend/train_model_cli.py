#!/usr/bin/env python
"""
Training script to train the resume matching model on random datasets.

Usage:
    python train_model_cli.py --samples 500
    python train_model_cli.py --samples 1000 --force
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from model_trainer import train_model, MODEL_PATH, VECTORIZER_PATH
except ImportError:
    from backend.model_trainer import train_model, MODEL_PATH, VECTORIZER_PATH

def main():
    parser = argparse.ArgumentParser(
        description='Train the resume matching model on random datasets'
    )
    parser.add_argument(
        '--samples',
        type=int,
        default=500,
        help='Number of training samples to generate (default: 500)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force retrain even if model exists'
    )
    
    args = parser.parse_args()
    
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH) and not args.force:
        print(f"Model already trained at {MODEL_PATH}")
        print("Use --force to retrain the model.")
        return 0
    
    try:
        print(f"\n{'='*60}")
        print("Resume Matching Model Training")
        print(f"{'='*60}\n")
        
        model, vectorizer = train_model(num_samples=args.samples)
        
        print(f"\n{'='*60}")
        print("[OK] Training Complete!")
        print(f"{'='*60}")
        print(f"Model saved to: {MODEL_PATH}")
        print(f"Vectorizer saved to: {VECTORIZER_PATH}")
        print(f"Samples used: {args.samples}")
        print(f"\nYou can now use the trained model for predictions.")
        print(f"API calls will automatically use the trained model if available.\n")
        
        return 0
    except Exception as e:
        print(f"\n[ERROR] Error during training: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
