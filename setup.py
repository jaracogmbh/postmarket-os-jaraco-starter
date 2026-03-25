from setuptools import setup

setup(
    name="jaraco-starter",
    version="0.1.0",
    package_dir={"": "src"},
    packages=["jaraco_starter"],
    entry_points={"console_scripts": ["jaraco-starter=jaraco_starter.app:main"]},
)
