from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from ai_engine.category_classifier import classifier
from ai_engine.priority_predictor import predictor
from ai_engine.duplicate_detector import find_duplicates
from problems.models import Problem
import json

@require_POST
def analyze_text(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        category = classifier.predict_with_confidence(text)
        priority = predictor.predict_with_confidence(
            text,
            duration=data.get('duration'),
            affected_count=data.get('affected_count'),
        )
        existing = Problem.objects.filter(status__in=['APPROVED', 'PENDING']).values_list('title', 'description')
        existing_texts = [f"{t[0]} {t[1]}" for t in existing]
        duplicates = find_duplicates(text, existing_texts, threshold=60)
        return JsonResponse({
            'category': category['label'],
            'category_confidence': category['confidence'],
            'priority': priority['label'],
            'priority_confidence': priority['confidence'],
            'duplicates': duplicates[:5],
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
