import setuptools


packages = setuptools.find_packages(
    include=[
        'paperful',
        'paperful.*',
    ],
)

setuptools.setup(
    author='David Joaquín Shourabi Porcel',
    author_email='david@djsp.eu',
    description='CLI for Paperless',
    entry_points={
        'console_scripts': [
            'paperful = paperful.cli.main:entry_point',
        ],
    },
    install_requires=[
        'pycups == 2.0.1',
        'pyxdg == 0.27',
        'requests == 2.26.0',
    ],
    name='paperful',
    packages=packages,
    python_requires='>= 3.9.7',
    url='https://github.com/kalrish/paperful',
    version='0.1',
)
