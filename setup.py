import os
import shutil
from setuptools import setup, find_packages

# Simple Procfile for Render/Heroku compatible deployment
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nail_salon',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,
)