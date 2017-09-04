from distutils.core import setup

setup(
    name='nexradaws',
    version='1.0.1',
    packages=['nexradaws','nexradaws.resources'],
    description= 'Query and download NEXRAD data from AWS S3 storage.',
    long_description= '''This module is designed to allow you to query and download Nexrad
radar files from Amazon Web Services S3 Storage. The real-time feed and full historical archive of original
resolution (Level II) NEXRAD data, from June 1991 to present, is now freely available on Amazon S3 for anyone to use.
More information can be found here https://aws.amazon.com/public-datasets/nexrad/.

If pyart is installed nexradaws allows you to quickly get pyart objects of downloaded files.

nexradaws supports Python 2.7 and Python 3.6.

Github - https://github.com/aarande/nexradaws

PyPi - https://pypi.python.org/pypi/nexradaws

Docs - http://nexradaws.readthedocs.io/en/latest/

**Required dependencies**

* boto3
* pytz
* six

**Optional dependencies**

* pyart

**Install with pip**::

    pip install nexradaws''',
    url='https://github.com/aarande/nexradaws',
    license='MIT',
    author='Aaron Anderson',
    author_email='aaron.anderson74@yahoo.com',
    keywords='weather,radar,nexrad,aws,amazon',
    download_url='https://github.com/aarande/nexradaws/archive/1.0.tar.gz',
    install_requires=['boto3','pytz','six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
