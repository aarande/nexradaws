[![Build Status](https://travis-ci.org/aarande/nexradaws.svg?branch=master)](https://travis-ci.org/aarande/nexradaws)   [![codecov](https://codecov.io/gh/aarande/nexradaws/branch/master/graph/badge.svg)](https://codecov.io/gh/aarande/nexradaws) [![Documentation Status](https://readthedocs.org/projects/nexradaws/badge/?version=latest)](http://nexradaws.readthedocs.io/en/latest/?badge=latest) [![Documentation Status](https://readthedocs.org/projects/nexradaws/badge/?version=devel)](http://nexradaws.readthedocs.io/en/devel/?badge=devel)
# nexradaws
This module is designed to allow you to query and download Nexrad
radar files from Amazon Web Services S3 Storage. The real-time feed and full historical archive of original
resolution (Level II) NEXRAD data, from June 1991 to present, is now freely available on Amazon S3 for anyone to use.
More information can be found here https://aws.amazon.com/public-datasets/nexrad/.

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

    pip install nexradaws

New in version 1.1:
* Better support for varying filenames over the years (Thanks Nick Guy for the PR!)
