import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from ai_engine.preprocessing import clean_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'category_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'category_vectorizer.pkl')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'ML_Project_Complaint_Dataset_Duration_Imp.csv')

CATEGORY_MAP = {
    'Mess/Food': 'Canteen',
    'Technical Issues': 'Infrastructure',
    'Academics': 'Other',
    'Ragging': 'Safety',
}

class CategoryClassifier:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                self.vectorizer = joblib.load(VECTORIZER_PATH)
                dataset = pd.read_csv(DATASET_PATH).dropna(subset=['category'])
                expected_labels = {
                    CATEGORY_MAP.get(value, value) for value in dataset['category'].unique()
                }
                if set(self.model.classes_) != expected_labels:
                    raise ValueError('Stored category model does not match the current dataset')
                self.model.predict_proba(self.vectorizer.transform(['model check']))
            except Exception:
                self.train()
        else:
            self.train()

    def train(self):
        df = pd.read_csv(DATASET_PATH).dropna(subset=['complaint_text', 'category'])
        df['category'] = df['category'].map(lambda value: CATEGORY_MAP.get(value, value))
        df['cleaned'] = df['complaint_text'].apply(clean_text)
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        X = self.vectorizer.fit_transform(df['cleaned'])
        y = df['category']
        self.model = LogisticRegression(max_iter=1000, class_weight='balanced')
        self.model.fit(X, y)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.vectorizer, VECTORIZER_PATH)

    def predict_with_confidence(self, text):
        if self.model is None or self.vectorizer is None:
            self.train()
        cleaned = clean_text(text)
        vec = self.vectorizer.transform([cleaned])
        pred = self.model.predict(vec)[0]
        proba = self.model.predict_proba(vec)[0].max()
        return {'label': pred, 'confidence': round(float(proba) * 100, 2)}

    def predict(self, text):
        return self.predict_with_confidence(text)['label']

classifier = CategoryClassifier()
