[![CI](https://github.com/aarande/nexradaws/actions/workflows/ci.yml/badge.svg)](https://github.com/aarande/nexradaws/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/aarande/nexradaws/branch/master/graph/badge.svg)](https://codecov.io/gh/aarande/nexradaws) [![Documentation Status](https://readthedocs.org/projects/nexradaws/badge/?version=latest)](http://nexradaws.readthedocs.io/en/latest/?badge=latest) [![Documentation Status](https://readthedocs.org/projects/nexradaws/badge/?version=devel)](http://nexradaws.readthedocs.io/en/devel/?badge=devel)
# nexradaws
This module is designed to allow you to query and download Nexrad
radar files from Amazon Web Services S3 Storage. The real-time feed and full historical archive of original
resolution (Level II) NEXRAD data, from June 1991 to present, is now freely available on Amazon S3 for anyone to use.
More information can be found here https://aws.amazon.com/public-datasets/nexrad/.

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
    pip install nexradaws[pyart] - to install with pyart support   

New in version 2.0:
* Updated to support Python 3.8+, dropped support for Python 2.7.
* Update to new bucket names for NEXRAD data.
* Fix for NoneType when time is in future

New in version 1.1:
* Bug fix for varying filename extensions over the years (.gz .V06 etc). Thanks Nick Guy for the PR!


