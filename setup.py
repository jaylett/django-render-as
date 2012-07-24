# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'django-render-as'
VERSION = '0.1'

package_data = {
    'render_as': [
        'templates/avoid_clash_with_real_app/*.html',
        'templates/render_as/*.html',
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
        'Django>=1.3',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
)
