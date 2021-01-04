from setuptools import setup, find_packages
from percolation import (__version__, __author__, __email__,
                         __directory__, __github__, __license__)

description_path = __directory__ / 'resources/misc/description.txt'
with open(description_path, 'r') as file:
    description = file.read()

setup(
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['numpy>=1.19.0, matplotlib>=3.3.3'],
    python_requires='>=3.9.0',
    name='Percolation',
    version=__version__,
    description=description,
    url=__github__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    keywords=['monte carlo', 'percolation', 'hoshen-kopelman'],
)
