import os
SECRET_KEY = 'fake-key'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework_swagger',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'fileApp.apps.FileAppConfig',
    'home.apps.HomeConfig'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ROOT_URLCONF = r'rtaa_gis.urls'
LOGIN_URL = r'login/'
LOGIN_REDIRECT_URL = r'/'
