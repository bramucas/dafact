import setuptools
from dafact import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dafact",
    version=__version__,
    author="Brais Muñiz",
    author_email="mc.brais@gmail.com",
    description="Encodes data as ASP facts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bramucas/dafact",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'logic programming',
        'answer set programming',
    ],
    python_requires='>=3.6.0',
    install_requires=[
        'clingo>=5.5.0.post3',
        'numpy',
        'argparse',
    ],
    packages=['dafact', 'dafact.encoders'],
    entry_points={'console_scripts': ['dafact=dafact.__main__:main']})
