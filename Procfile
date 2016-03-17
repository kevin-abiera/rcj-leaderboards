web: gunicorn config.wsgi:application
worker: celery worker --app=leaderboards.taskapp --loglevel=info
