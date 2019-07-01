from setuptools import setup, find_packages, findall

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

packages = find_packages(include=('nonebot', 'nonebot.*'))
stub_files = list(filter(lambda x: x.endswith('.pyi'), findall('nonebot')))

setup(
    name='nonebot',
    version='1.3.1',
    url='https://github.com/richardchien/nonebot',
    license='MIT License',
    author='Richard Chien',
    author_email='richardchienthebest@gmail.com',
    description='An asynchronous QQ bot framework based on CoolQ.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    data_files=stub_files,
    install_requires=['aiocqhttp>=0.6.8', 'aiocache>=0.10'],
    extras_require={
        'scheduler': ['apscheduler>=1.2'],
    },
    python_requires='>=3.6.1',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
