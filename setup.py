from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='none-bot',
    version='0.1.0',
    packages=find_packages(include=('none', 'none.*')),
    url='https://github.com/richardchien/none-bot',
    license='MIT License',
    author='Richard Chien',
    author_email='richardchienthebest@gmail.com',
    description='A QQ bot framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['aiocqhttp>=0.6', 'aiocache>=0.10'],
    python_requires='>=3.6',
    platforms='any',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
