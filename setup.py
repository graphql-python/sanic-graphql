from setuptools import setup, find_packages

required_packages = [
    'graphql-core>=1.0',
    'graphql-server-core>=1.0.dev',
    'sanic>=0.5.1',
    'pytest-runner'
]

setup(
    name='Sanic-GraphQL',
    version='1.1.0',
    description='Adds GraphQL support to your Sanic application',
    long_description=open('README.rst').read(),
    url='https://github.com/graphql-python/sanic-graphql',
    download_url='https://github.com/graphql-python/sanic-graphql/releases',
    author='Sergey Porivaev',
    author_email='porivaevs@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='api graphql protocol sanic',
    packages=find_packages(exclude=['tests']),
    install_requires=required_packages,
    tests_require=['pytest>=2.7.3', 'aiohttp>=1.3.0', 'yarl>=0.9.6', 'jinja2>=2.9.0'],
    include_package_data=True,
    platforms='any',
)
