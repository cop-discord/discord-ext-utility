from setuptools import setup, find_packages
with open("requirements.txt", "r") as file:
    requirements = file.readlines()

packages = [
    "discord.ext.utility",
    "discord.ext.utility.converters",

]

setup(
    name = "discord-ext-utility",
    version = "0.0.1",
    description = "a library with miscellaneous discord.py/disdick utilities and overwrites to make your discord bot better and more user-friendly",
    author = "cop",
    author_email = "cop@catgir.ls",
    packages = packages,
    include_package_data = True,
    package_data={'discord.ext.utility': ['*.pkl']},
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ],
)   