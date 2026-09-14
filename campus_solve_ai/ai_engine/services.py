from ai_engine.category_classifier import classifier
from ai_engine.priority_predictor import predictor
from ai_engine.duplicate_detector import find_duplicates
from problems.models import Problem

def analyze_problem(title, description, exclude_id=None, duration=None, affected_count=None):
    text = f"{title} {description}"
    category = classifier.predict_with_confidence(text)
    priority = predictor.predict_with_confidence(text, duration, affected_count)
    qs = Problem.objects.filter(status__in=['APPROVED', 'PENDING'])
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    existing_texts = [f"{p.title} {p.description}" for p in qs]
    duplicates = find_duplicates(text, existing_texts, threshold=60)
    problems = list(qs)
    duplicate_records = []
    for dup in duplicates:
        duplicate_records.append({
            'problem': problems[dup['index']],
            'score': dup['score'],
        })
    return {
        'category': category['label'],
        'category_confidence': category['confidence'],
        'priority': priority['label'],
        'priority_confidence': priority['confidence'],
        'duplicates': duplicate_records,
    }
