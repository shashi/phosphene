import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "phosphene",
    version = "0.0.1",
    author = "Shashi Gowda",
    author_email = "shashigowda91@gmail.com",
    description = ("A library for music processing and visualization"),
    license = "MIT",
    keywords = "music audio dsp visualization",
    url = "https://github.com/shashi/phosphene",
    packages=["phosphene"],
    long_description=read("../README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "License :: OSI Approved :: MIT License",
    ],
)
