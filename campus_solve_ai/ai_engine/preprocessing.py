import re

STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'for',
    'from', 'has', 'have', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the',
    'this', 'to', 'was', 'were', 'with',
}

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text).lower())
    tokens = text.split()
    tokens = [token for token in tokens if token not in STOP_WORDS]
    return ' '.join(tokens)
