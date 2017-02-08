# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'django-render-as'
VERSION = '1.2'

package_data = {
    'render_as': [
        'test_templates/avoid_clash_with_real_app/*.html',
        'test_templates/render_as/*.html',
        ],
}

setup(
    name=PACKAGE, version=VERSION,
    description="Template rendering indirector based on object class",
    packages=[
        'render_as',
        'render_as/templatetags',
        ],
    package_data=package_data,
    license='MIT',
    author='James Aylett',
    author_email='james@tartarus.org',
    install_requires=[
        'Django~=1.10',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
