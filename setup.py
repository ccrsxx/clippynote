from setuptools import setup

setup(
    name='notepy',
    version='0.1.0',
    description='A simple CLI for taking notes',
    author='ccrsxx',
    author_email='aminrisal@gmail.com',
    packages=['notepy'],
    entry_points={'console_scripts': ['notepy=notepy.cli:main']},
    install_requires=[],
)
