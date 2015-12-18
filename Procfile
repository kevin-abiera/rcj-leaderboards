web: gunicorn config.wsgi:application
worker: celery worker --app=rcj-leaderboards.taskapp --loglevel=info
