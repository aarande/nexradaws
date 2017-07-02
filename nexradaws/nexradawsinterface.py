import os
import re
from datetime import timedelta

import boto3
import errno
import pytz
import six
from botocore.handlers import disable_signing

from .responses.nexradawsfile import NexradAwsFile


class NexradAwsInterface(object):
    def __init__(self):
        self._year_re = re.compile('^(\d{4})/')
        self._month_re = re.compile('^\d{4}/(\d{2})')
        self._day_re = re.compile('^\d{4}/\d{2}/(\d{2})')
        self._radar_re = re.compile('^\d{4}/\d{2}/\d{2}/(....)/')
        self._scan_re = re.compile('^\d{4}/\d{2}/\d{2}/..../(.*.gz)')
        self._s3conn = boto3.resource('s3')
        self._s3conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        self._bucket = self._s3conn.Bucket('noaa-nexrad-level2')

    def get_available_years(self):
        """
        This method allows you to get the years that are currently available.
        :rtype : list
        :return: A list of strings representing the years available
        """
        years = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',Delimiter='/')
        for each in resp.get('CommonPrefixes'):
            match = self._year_re.match(each.get('Prefix'))
            if match is not None:
                years.append(match.group(1))
        return years

    def get_available_months(self, year):
        """
        This method allows you to get the available months in a given year.
        :rtype : list
        :param year: string - the year we are requesting available months for (i.e. 2010)
        :return: A list of strings representing the months available for that year
        """
        months = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',
                                                     Prefix='{}/'.format(year),
                                                     Delimiter='/')
        for each in resp.get('CommonPrefixes'):
            match = self._month_re.match(each.get('Prefix'))
            if match is not None:
                months.append(match.group(1))
        return months

    def get_available_days(self, year, month):
        """
        This method allows you to get the available days in a given month and year.
        :rtype : list
        :param year: string - the year we are requesting available days for (i.e 2010)
        :param month: string - the month we are requesting available days for (i.e. 05)
        :return: A list of strings representing the days available in the given month and year
        """
        days = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',
                                                     Prefix='{}/{}/'.format(year,month),
                                                     Delimiter='/')
        for each in resp.get('CommonPrefixes'):
            match = self._day_re.match(each.get('Prefix'))
            if match is not None:
                days.append(match.group(1))
        return days

    def get_available_radars(self, year, month, day):
        """
        This method allows you to get the available radars in a given day, month, and year.
        :rtype : list
        :param year: string - the year we are requesting available radars for (i.e 2010)
        :param month: string - the month we are requesting available radars for (i.e. 05)
        :param day: string - the day we are requesting available radars for (i.e. 01)
        :return: A list of string representing the radar sites available in the given
        day, month, and year
        """
        radars = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',
                                                     Prefix='{}/{}/{}/'.format(year,month,day),
                                                     Delimiter='/')
        for each in resp.get('CommonPrefixes'):
            match = self._radar_re.match(each.get('Prefix'))
            if match is not None:
                radars.append(match.group(1))
        return radars

    def get_available_scans(self, year, month, day, radar):
        """
        This method allows you to get the available radar scans for a given radar, day, month, and year.
        :rtype : list
        :param year: string - the year we are requesting available scans for (i.e 2010)
        :param month: string - the month we are requesting available scans for (i.e. 05)
        :param day: string - the day we are requesting available scans for (i.e. 01)
        :param radar: string - the radar id we are requesting available scans for (i.e. KTLX)
        :return: NexradAwsFile - A list of NexradAwsFile objects representing the radar scans available for a given radar,
        day, month, and year
        """
        scans = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',
                                                     Prefix='{}/{}/{}/{}/'.format(year,month,day,radar),
                                                     Delimiter='/')
        for scan in resp.get('Contents'):
            match = self._scan_re.match(scan.get('Key'))
            if match is not None:
                scans.append(NexradAwsFile(scan))
        return scans

    def get_available_scans_in_range(self, start, end, radar):
        """
        Get all available scans for a radar between start and end date.
        If datetime's do not include a timezone they will be set to UTC.
        :param start: datetime - start time for range
        :param end: datetime - end time for range
        :param radar: string - radar id
        :return: NexradAwsFile - A list of NexradAwsFile objects representing the radar scans available in the passed
        time range.
        """
        scans = []
        utcstart,utcend = self._formattimerange(start,end)
        for day in self._datetime_range(utcstart,utcend):
            availscans = self.get_available_scans('{0:0>2}'.format(day.year),
                                     '{0:0>2}'.format(day.month),
                                     '{0:0>2}'.format(day.day),
                                     radar.upper())
            for scan in availscans:
                if self._is_within_range(utcstart,utcend,scan.scan_time):
                    scans.append(scan)
        return scans

    def download(self, nexradawsfiles, basepath, keep_aws_folders=False):
        """
        This method will download the passed NexradAwsFile object(s) to the given basepath folder.
        If keep_aws_folders is True then subfolders will be created under the basepath with the same
         structure as on AWS (year/month/day/radar/).
        :param nexradawsfiles: a single NexradAwsFile or a list of NexradAwsFile objects to download
        :param basepath: string - location to save downloaded files
        :param keep_aws_folders: boolean - weather or not to use the aws folder structure
         inside the basepath...(yeah/month/day/radar/)
        """
        if isinstance(nexradawsfiles,list):
            for awsfile in nexradawsfiles:
                dirpath,filepath = awsfile.create_filepath(basepath, keep_aws_folders)
                self._make_directories(dirpath)
                self._bucket.download_file(awsfile.key, filepath)
        else:
            dirpath, filepath = nexradawsfiles.create_filepath(basepath, keep_aws_folders)
            self._make_directories(dirpath)
            self._bucket.download_file(nexradawsfiles.key, filepath)

    def _make_directories(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _datetime_range(self, start=None, end=None):
        span = end - start
        for i in range(0,span.days + 1):
            yield start + timedelta(days=i)

    def _is_within_range(self,start,end,value):
        if value >= start and value <= end:
            return True
        else:
            return False

    def _is_tzaware(self,d):
        if d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None:
            return True
        else:
            return False

    def _formattimerange(self,start,end):
        if self._is_tzaware(start):
            if start.tzinfo != pytz.UTC:
                utcstart = start.astimezone(pytz.UTC)
            else:
                utcstart = start
        else:
            utcstart = pytz.utc.localize(start)
        if self._is_tzaware(end):
            if end.tzinfo != pytz.UTC:
                utcend = end.astimezone(pytz.UTC)
            else:
                utcend = end
        else:
            utcend = pytz.utc.localize(end)
        return utcstart,utcend


