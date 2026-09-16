# Deploying CampusSolve AI on Vercel

Vercel detects this Django project from `campus_solve_ai/manage.py`; no legacy `api/` proxy or rewrite is required.

## 1. Create persistent storage

Create a Vercel Postgres/Neon database from the Vercel **Storage** tab and connect it to this project. This supplies `DATABASE_URL`. Do not use SQLite in production: Vercel functions have an ephemeral filesystem.

## 2. Add environment variables

In **Project Settings → Environment Variables**, add these to Production (and Preview if needed):

| Variable | Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | A long random Django secret |
| `DATABASE_URL` | The connected PostgreSQL/Neon connection string |
| `ALLOWED_HOSTS` | `your-project.vercel.app,yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-project.vercel.app,https://yourdomain.com` |

Use comma-separated values without spaces. `VERCEL_URL` is supplied automatically by Vercel.

## 3. Deploy

Push the project to GitHub and import it at Vercel with the **Root Directory** set to `campus_solve_ai` (the folder containing `manage.py`, `requirements.txt`, and `vercel.json`). Vercel detects Django automatically.

After the first deployment, run migrations once against the production database:

```bash
vercel env pull .env.production.local
python campus_solve_ai/manage.py migrate --settings=campus_solve_ai.settings.production
python campus_solve_ai/manage.py createsuperuser --settings=campus_solve_ai.settings.production
```

Run the migrate command again whenever a new migration is added.

## Important: uploaded images

The current `MEDIA_ROOT` filesystem is temporary on Vercel. Problem-image uploads need object storage (Vercel Blob, S3, or Cloudinary) before production use.
