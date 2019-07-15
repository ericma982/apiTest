try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='api',  # Required
    version='1.0.1',  # Required
    description='A sample Python Flask API project for snapcraft',  # Optional
    packages=find_packages(),  # Required
    zip_safe = False,
    install_requires=['Flask', 'flask_restplus', 'docopt'],
    python_requires='>=3.5, <4',
    scripts = ['bin/apiExe.py'],

)
