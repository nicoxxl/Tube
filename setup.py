from setuptools import setup, find_packages

SRC_DIR = "tube"

setup(
    name="Tube",
    version="0.1",
    description="Something, something, pipe related joke, something",
    author="Nicolas B.",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
)
