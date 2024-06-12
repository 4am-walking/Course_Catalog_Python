from setuptools import setup

setup(
    name="pycatalog",
    version="0.1.0",
    packages=["pycatalog"],
    install_requires=[
        "urllib3",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "pycatalog = pycatalog.cli:main",
        ],
    },
)
