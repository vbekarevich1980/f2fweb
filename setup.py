try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My first game Face-To-Face',
    'author': 'Vitali Bekarevich',
    'url': 'http://10.10.10.140/',
    'download_url': 'Where to download it.',
    'author_email': 'vbekarevich1980@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['f2fweb'],
    'scripts': [],
    'name': 'f2fweb'
    }

setup(**config)
