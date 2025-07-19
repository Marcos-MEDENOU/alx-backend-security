# ... other settings ...

# Rate limiting settings
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_ENABLE = True

# Cache settings for rate limiting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Add 'ratelimit' to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your other apps ...
    'ratelimit',
    'ip_tracking',
]

ROOT_URLCONF = 'urls'

# Configuration Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Cache settings for rate limiting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Add 'ratelimit' to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your other apps ...
    'ratelimit',
    'ip_tracking',
]

ROOT_URLCONF = 'urls'

# ... rest of your settings ...