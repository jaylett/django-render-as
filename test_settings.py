# Very simple Django settings file for testing
import os.path

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        },
}

SECRET_KEY = "django_render_as_test_key"

TEMPLATE_DEBUG = True
INSTALLED_APPS = [ 'render_as' ]
TEMPLATE_DIRS = [ os.path.join(os.path.dirname(os.path.realpath(__file__)), 'render_as', 'test_templates') ]
