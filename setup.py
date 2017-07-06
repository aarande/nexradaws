from distutils.core import setup

setup(
    name='nexradaws',
    version='1.0',
    packages=['nexradaws','nexradaws.resources'],
    url='https://github.com/aarande/nexradaws',
    license='MIT',
    author='Aaron Anderson',
    author_email='',
    description='This python package is designed to provide an interface to query and download NEXRAD archive data available on Amazon Web Services'
)
