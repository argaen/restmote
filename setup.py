from distutils.core import setup

packages = [ 'Django', ]

setup(
    name="django_restmote",
    version="0.1",
    url='http://github.com/argaen/django_restmote',
    license='Apache 2.0',
    description='Sync django databases from REST API.',
    author='Manu',
    author_email='manu.mirandad@gmail.com',
    install_requires=packages,
)
