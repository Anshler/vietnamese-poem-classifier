from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="vietnamese-poem-classifier",
    version="0.1.6",
    description="Classify genre and score Vietnamese poems",
    url="https://github.com/Anshler/vietnamese-poem-classifier",
    author="Huynh Minh Triet",
    author_email="huynhminhtriet2002@gmail.com",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    keywords="poem",
    packages=find_packages(),
    package_data={'vietnamese_poem_classifier': ['rhymes.txt','start_vowels.txt']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "transformers",
        "importlib",
        "importlib-resources",
    ],
    entry_points={
        "console_scripts": ["vietnamese-poem-classifier=vietnamese_poem_classifier:main"],
    },
)
