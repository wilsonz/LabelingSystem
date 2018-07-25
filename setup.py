# Note:
# This file should always be done at the start of projects.
# The setup file describe the project.
#
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    # /packages/    tells py what pkg dir to include.
    # find_packages():    finds these dir automatically so no need to
    #                     type them out.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', ],
)
