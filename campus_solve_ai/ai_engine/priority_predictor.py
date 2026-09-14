import os
import joblib
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from ai_engine.preprocessing import clean_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'priority_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'priority_vectorizer.pkl')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'ML_Project_Complaint_Dataset_Duration_Imp.csv')

class PriorityPredictor:
    def __init__(self):
        self.vectorizer = None
        self.metadata_encoder = None
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                saved = joblib.load(VECTORIZER_PATH)
                self.vectorizer = saved['text']
                self.metadata_encoder = saved['metadata']
                self.model.predict(self._features('model check', 'Unknown', 'Unknown'))
            except Exception:
                self.train()
        else:
            self.train()

    def train(self):
        df = pd.read_csv(DATASET_PATH).dropna(subset=['complaint_text', 'urgency'])
        df['cleaned'] = df['complaint_text'].apply(clean_text)
        df['duration'] = df['duration'].fillna('Unknown').astype(str)
        df['affected_count'] = df['affected_count'].fillna('Unknown').astype(str)
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        X = self.vectorizer.fit_transform(df['cleaned'])
        self.metadata_encoder = OneHotEncoder(handle_unknown='ignore')
        metadata = self.metadata_encoder.fit_transform(df[['duration', 'affected_count']])
        X = hstack([X, metadata]).tocsr()
        y = df['urgency']
        self.model = LogisticRegression(max_iter=1000, class_weight='balanced')
        self.model.fit(X, y)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump({'text': self.vectorizer, 'metadata': self.metadata_encoder}, VECTORIZER_PATH)

    def _features(self, text, duration, affected_count):
        text_features = self.vectorizer.transform([clean_text(text)])
        metadata = self.metadata_encoder.transform(pd.DataFrame([{
            'duration': str(duration or 'Unknown'),
            'affected_count': str(affected_count or 'Unknown'),
        }]))
        return hstack([text_features, metadata]).tocsr()

    def predict_with_confidence(self, text, duration=None, affected_count=None):
        if self.model is None or self.vectorizer is None or self.metadata_encoder is None:
            self.train()
        features = self._features(text, duration, affected_count)
        pred = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0].max()
        return {'label': pred, 'confidence': round(float(proba) * 100, 2)}

    def predict(self, text, duration=None, affected_count=None):
        return self.predict_with_confidence(text, duration, affected_count)['label']

predictor = PriorityPredictor()
