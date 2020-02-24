from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

packages = find_packages(include=('nonebot', 'nonebot.*'))

setup(
    name='nonebot',
    version='1.4.2',
    url='https://github.com/richardchien/nonebot',
    license='MIT License',
    author='Richard Chien',
    author_email='richardchienthebest@gmail.com',
    description='An asynchronous QQ bot framework based on CoolQ.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    package_data={
        '': ['*.pyi'],
    },
    install_requires=['aiocqhttp>=1.2,<1.3', 'aiocache>=0.10,<1.0'],
    extras_require={
        'scheduler': ['apscheduler'],
    },
    python_requires='>=3.7',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
