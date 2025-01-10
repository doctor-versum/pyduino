from setuptools import setup, find_packages

setup(
    name="pyduino",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyserial>=3.4",  # Falls nicht schon installiert, für die Kommunikation mit Arduino
    ],
    author="Dein Name",
    author_email="deine.email@example.com",
    description="Python-Bibliothek für die Kommunikation mit Arduino Uno R3 über serielle Schnittstelle",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/DeinGithubUser/pyduino",  # URL zu deinem GitHub-Repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Mindestens Python 3.6
)