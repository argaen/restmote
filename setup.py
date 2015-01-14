from distutils.core import setup

packages = [ 'Django', ]

setup(
    name="restmote",
    version="0.1.2",
    url='http://github.com/argaen/restmote',
    license='Apache 2.0',
    description='Sync local databases from REST API.',
    author='Manu',
    author_email='manu.mirandad@gmail.com',
    packages=['restmote'],
    install_requires=packages,
)
