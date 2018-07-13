.. nexradaws documentation master file, created by
   sphinx-quickstart on Wed Oct 28 15:02:11 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the nexradaws module documentation
#############################################

This module is designed to allow you to query and download Nexrad
radar files from Amazon Web Services S3 Storage. The real-time feed and full historical archive of original
resolution (Level II) NEXRAD data, from June 1991 to present, is now freely available on Amazon S3 for anyone to use.
More information can be found here https://aws.amazon.com/public-datasets/nexrad/.

nexradaws supports Python 2.7 and Python 3.6.

Github - https://github.com/aarande/nexradaws

PyPi - https://pypi.python.org/pypi/nexradaws

**Required dependencies**

* boto3
* pytz
* six

**Optional dependencies**

* pyart

**Install with pip**::

    pip install nexradaws


**Source Code**

The source code for nexradaws is available on Github `here <https://github.com/aarande/nexradaws>`_. Tickets can also be
opened here for any issues or enhancements requests.

Please feel free to submit Pull Requests for any fixes or enhancements.

**New in Version 1.1**

* Better support for varying filenames over the years (Thanks Nick Guy for the PR!)

Contents:

.. toctree::
   :maxdepth: 2

   apidocs
   Tutorial.ipynb

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

