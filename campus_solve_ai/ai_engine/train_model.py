import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_solve_ai.settings')
django.setup()

from ai_engine.category_classifier import CategoryClassifier
from ai_engine.priority_predictor import PriorityPredictor

if __name__ == '__main__':
    print("Training Category Classifier...")
    cat = CategoryClassifier()
    cat.train()
    print("Category Classifier trained and saved.")

    print("Training Priority Predictor...")
    pri = PriorityPredictor()
    pri.train()
    print("Priority Predictor trained and saved.")

    print("All models trained successfully.")
