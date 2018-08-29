import os.path
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    DEBUG=True,
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'render_as',
                    'test_templates',
                ),
            ],
            'APP_DIRS': False,
            'OPTIONS': {
                'debug': True,
            },
        },
    ],
    INSTALLED_APPS=[
        'render_as',
    ],
    DATABASES={
        'default': {
             'ENGINE': 'django.db.backends.sqlite3',
        }
    },
)


if hasattr(django, 'setup'):
    django.setup()


test_runner = DiscoverRunner(verbosity=1, failfast=False)
failures = test_runner.run_tests(['render_as', ])
if failures:  # pragma no cover
    sys.exit(failures)
