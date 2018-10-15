from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='none-bot',
    version='0.4.0',
    packages=find_packages(include=('none', 'none.*')),
    url='https://github.com/richardchien/none-bot',
    license='MIT License',
    author='Richard Chien',
    author_email='richardchienthebest@gmail.com',
    description='An asynchronous QQ bot framework based on CoolQ.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['aiocqhttp>=0.6', 'aiocache>=0.10'],
    extras_require={
        'scheduler': ['apscheduler>=1.2'],
    },
    python_requires='>=3.6',
    platforms='any',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)
