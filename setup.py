from setuptools import setup, find_packages

required_packages = ['graphql-core>=1.0', 'sanic>=0.3.1']

setup(
    name='Sanic-GraphQL',
    version='0.3.1',
    description='Adds GraphQL support to your Sanic application',
    long_description=open('README.rst').read(),
    url='https://github.com/grazor/sanic-graphql',
    download_url='https://github.com/grazor/sanic-graphql/releases',
    author='Sergey Porivaev',
    author_email='porivaevs@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='api graphql protocol sanic',
    packages=find_packages(exclude=['tests']),
    install_requires=required_packages,
    tests_require=['pytest>=2.7.3', 'aiohttp', 'yarl==0.8.1'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
)
