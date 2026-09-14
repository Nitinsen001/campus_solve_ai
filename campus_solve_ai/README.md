# CampusSolve AI

Anonymous AI-Powered Campus Problem Reporting and Collaborative Solution Platform

## Project Overview

CampusSolve AI is a modern, full-stack Django web application that enables college students to anonymously report campus-related problems and collaboratively suggest solutions. The system leverages Machine Learning and NLP for automatic problem categorization, priority prediction, and duplicate detection. All submissions require admin moderation before becoming public.

## Technology Stack

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Database:** MySQL
- **ML/NLP:** Scikit-learn, Pandas, NumPy, NLTK, TF-IDF, Cosine Similarity, Logistic Regression
- **Analytics:** Chart.js

## Features

- Anonymous problem reporting with AI-powered category classification
- Priority prediction based on NLP analysis
- Duplicate problem detection using cosine similarity
- Admin moderation panel with AI prediction review
- Community solution system with recommendation features
- Real-time analytics dashboard
- Role-based access control (Student / Admin)
- Responsive modern UI

## Installation

1. Clone or extract the project:
   ```
   cd campus_solve_ai
   ```

2. Create a MySQL database:
   ```sql
   CREATE DATABASE campus_solve_ai;
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Train the ML models:
   ```bash
   python ai_engine/train_model.py
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Visit http://127.0.0.1:8000/

## Usage

- **Students:** Register, report problems, browse approved problems, submit solutions
- **Admin:** Moderate problems/solutions, view analytics, manage categories

## Project Structure

```
campus_solve_ai/
├── accounts/           # User authentication and profiles
├── problems/           # Problem submission, feed, and moderation
├── solutions/          # Solution submission and management
├── analytics/          # Analytics models and dashboard
├── ai_engine/          # ML/NLP modules
│   ├── preprocessing.py
│   ├── category_classifier.py
│   ├── priority_predictor.py
│   ├── duplicate_detector.py
│   ├── services.py
│   └── train_model.py
├── dashboard/          # Admin dashboard
├── templates/          # Global HTML templates
├── static/             # Global CSS and JS
└── campus_solve_ai/    # Django project settings
```

## Anonymous Identity Policy

- All public-facing problems and solutions display: "Anonymous Campus Member"
- Real names, emails, and IDs are never exposed on the public platform
- Identity data is stored securely for authentication and abuse prevention only

## AI/ML Features

1. **Category Classification:** TF-IDF + Logistic Regression
2. **Priority Prediction:** NLP-based priority scoring
3. **Duplicate Detection:** Cosine similarity on TF-IDF vectors

## License

MIT License
Superuser created: admin@campussolve.ai / admin123