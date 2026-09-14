from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai_engine.preprocessing import clean_text

def calculate_similarity(text1, text2):
    cleaned1 = clean_text(text1)
    cleaned2 = clean_text(text2)
    if not cleaned1 or not cleaned2:
        return 0.0
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([cleaned1, cleaned2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(similarity) * 100, 2)

def find_duplicates(new_text, existing_texts, threshold=60):
    cleaned_new = clean_text(new_text)
    cleaned_existing = [clean_text(text) for text in existing_texts]
    if not cleaned_new or not cleaned_existing:
        return []
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([cleaned_new, *cleaned_existing])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel() * 100
    results = [
        {'index': idx, 'score': round(float(score), 2), 'text': existing_texts[idx]}
        for idx, score in enumerate(scores)
        if score >= threshold
    ]
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
