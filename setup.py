import subprocess
import sys

import setuptools


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='deezer-dl',
    version='1.0.0',
    author='Bruno Kanazawa',
    author_email='kanazawabruno@gmail.com',
    python_requires='>=3',
    install_requires=requirements,
    description="Download songs from Deezer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doulwyi/deezer-dl",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'deezer_dl = deezer_dl.deezer_dl:deezer_dl',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


install('git+https://github.com/nficano/pytube.git')