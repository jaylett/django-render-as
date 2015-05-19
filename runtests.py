import os.path
import sys

import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    TEMPLATE_DEBUG = True,
    TEMPLATE_DIRS = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'render_as', 'test_templates'),
    ],
    INSTALLED_APPS = [
        'render_as',
    ],
    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.sqlite3',
        }
    },
)

if hasattr(django, 'setup'):
    django.setup()

from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner(verbosity=1, failfast=False)
failures = test_runner.run_tests(['render_as', ])
if failures: #pragma no cover
    sys.exit(failures)
