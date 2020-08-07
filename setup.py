from setuptools import setup, find_packages

install_requires = [
    "graphql-server[sanic]>=3.0.0b1",
]

tests_requires = [
    "pytest>=5.4,<5.5",
    "pytest-asyncio>=0.11.0",
    "pytest-cov>=2.8,<3",
    "aiohttp>=3.5.0,<4",
    "Jinja2>=2.10.1,<3",
]

dev_requires = [
    "flake8>=3.7,<4",
    "isort>=4,<5",
    "check-manifest>=0.40,<1",
] + tests_requires

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="Sanic-GraphQL",
    version="1.2.0",
    description="Adds GraphQL support to your Sanic application",
    long_description=readme,
    url="https://github.com/graphql-python/sanic-graphql",
    download_url="https://github.com/graphql-python/sanic-graphql/releases",
    author="Sergey Porivaev",
    author_email="porivaevs@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="api graphql protocol sanic",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require={
        'test': tests_requires,
        'dev': dev_requires,
    },
    include_package_data=True,
    zip_safe=False,
    platforms="any",
)
