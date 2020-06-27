from setuptools import setup, find_packages

required_packages = [
    "graphql-core>=2.1,<3",
    "graphql-server-core>=1.1.1,<2",
    "sanic>=0.5.1,<19",
]

tests_require = ["pytest>=2.7.3", "aiohttp>=3.5.0,<4", "yarl>=1.0,<2.0", "Jinja2>=2.10.1"]

setup(
    name="Sanic-GraphQL",
    version="1.2.0",
    description="Adds GraphQL support to your Sanic application",
    long_description=open("README.rst", encoding="utf-8").read(),
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
    install_requires=required_packages,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    include_package_data=True,
    platforms="any",
)
