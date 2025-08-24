import setuptools

setuptools.setup(
    name='nexradaws',
    version='2.0.0',
    packages=['nexradaws','nexradaws.resources'],
    description= 'Query and download NEXRAD data from AWS S3 storage.',
    long_description= '''This module is designed to allow you to query and download Nexrad
radar files from Amazon Web Services S3 Storage. The real-time feed and full historical archive of original
resolution (Level II) NEXRAD data, from June 1991 to present, is now freely available on Amazon S3 for anyone to use.
More information can be found here https://aws.amazon.com/public-datasets/nexrad/.

If pyart is installed nexradaws allows you to quickly get pyart objects of downloaded files.

nexradaws supports Python 3.8+.

Github - https://github.com/aarande/nexradaws

PyPi - https://pypi.python.org/pypi/nexradaws

Docs - http://nexradaws.readthedocs.io/en/latest/

**Required dependencies**

* boto3
* pytz

**Optional dependencies**

* pyart

**Install with pip**::

    pip install nexradaws

**Version 2.0.0**
* Drop support for Python 2.7 and remove dependency on six.
* Bug fix for varying filename extensions over the years (.gz .V06 etc). Thanks Nick Guy for the PR!''',
    url='https://github.com/aarande/nexradaws',
    license='MIT',
    author='Aaron Anderson',
    author_email='aaron.anderson74@yahoo.com',
    keywords='weather,radar,nexrad,aws,amazon',
    download_url='https://github.com/aarande/nexradaws/archive/2.0.0.tar.gz',
    install_requires=['boto3','pytz'],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
