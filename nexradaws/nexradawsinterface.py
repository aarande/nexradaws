import os
import re
from datetime import timedelta

import boto3
import errno
import pytz
import six
from botocore.handlers import disable_signing

from .resources.downloadresults import DownloadResults
from .resources.localnexradfile import LocalNexradFile
from .resources.awsnexradfile import AwsNexradFile
import concurrent.futures

class NexradAwsInterface(object):
    """
    Instantiate an instance of this class to get a connection to the Nexrad AWS bucket. \
    This class provides methods to query for various metadata of the AWS bucket as well \
    as download files.

    >>> import nexradaws
    >>> conn = nexradaws.NexradAwsInterface()

    """
    def __init__(self):
        super(NexradAwsInterface, self).__init__()
        self._year_re = re.compile(r'^(\d{4})/')
        self._month_re = re.compile(r'^\d{4}/(\d{2})')
        self._day_re = re.compile(r'^\d{4}/\d{2}/(\d{2})')
        self._radar_re = re.compile(r'^\d{4}/\d{2}/\d{2}/(....)/')
        self._scan_re = re.compile(r'^\d{4}/\d{2}/\d{2}/..../(.*.gz)')
        self._s3conn = boto3.resource('s3')
        self._s3conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        self._bucket = self._s3conn.Bucket('noaa-nexrad-level2')

    def get_avail_years(self):
        """
        This method allows you to get the years that are currently available.

        >>> print conn.get_avail_years()
        >>> [u'1991', u'1992', u'1993', u'1994', u'1995', u'1996', u'1997', u'1998', u'1999', u'2000', u'2001', u'2002', u'2003', u'2004', u'2005', u'2006', u'2007', u'2008', u'2009', u'2010', u'2011', u'2012', u'2013', u'2014', u'2015', u'2016', u'2017']

        :return: A list of strings representing the years available
        :rtype list:

        """
        years = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',Delimiter='/')
        for each in resp.get('CommonPrefixes'):
            match = self._year_re.match(each.get('Prefix'))
            if match is not None:
                years.append(match.group(1))
        return years

    def get_avail_months(self, year):
        """
        This method allows you to get the available months in a given year.

        >>> print conn.get_avail_months('2013')
        >>> [u'01', u'02', u'03', u'04', u'05', u'06', u'07', u'08', u'09', u'10', u'11', u'12']


        :param year: the year we are requesting available months for (i.e. 2010)
        :type year: str
        :return: A list of strings representing the months available for that year
        :rtype list:

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

    def get_avail_days(self, year, month):
        """
        This method allows you to get the available days in a given year and month.

        >>> print conn.get_avail_days('2013','05')
        >>> [u'01', u'02', u'03', u'04', u'05', u'06', u'07', u'08', u'09', u'10', u'11', u'12', u'13', u'14', u'15', u'16', u'17', u'18', u'19', u'20', u'21', u'22', u'23', u'24', u'25', u'26', u'27', u'28', u'29', u'30', u'31']

        :param year: the year we are requesting available days for (i.e 2010)
        :type year: str
        :param month: the month we are requesting available days for (i.e. 05)
        :type month: str
        :return: A list of strings representing the days available in the given month and year
        :rtype list:

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

    def get_avail_radars(self, year, month, day):
        """
        This method allows you to get the available radars in a given year, month, and day.

        >>> print conn.get_avail_radars('2013','05','31')
        >>> [u'DAN1', u'KABR', u'KABX', u'KAKQ', u'KAMA', u'KAMX', u'KAPX', u'KARX', u'KATX', u'KBBX', u'KBGM', u'KBHX', u'KBIS', u'KBLX', u'KBMX', u'KBOX', u'KBRO', u'KBUF', u'KBYX', u'KCAE', u'KCBW', u'KCBX', u'KCCX', u'KCLE', u'KCLX', u'KCRP', u'KCXX', u'KCYS', u'KDAX', u'KDDC', u'KDFX', u'KDGX', u'KDLH', u'KDMX', u'KDOX', u'KDTX', u'KDVN', u'KEAX', u'KEMX', u'KENX', u'KEOX', u'KEPZ', u'KESX', u'KEVX', u'KEWX', u'KEYX', u'KFCX', u'KFDR', u'KFFC', u'KFSD', u'KFSX', u'KFTG', u'KFWS', u'KGGW', u'KGJX', u'KGLD', u'KGRB', u'KGRK', u'KGRR', u'KGSP', u'KGWX', u'KGYX', u'KHDX', u'KHGX', u'KHNX', u'KHPX', u'KHTX', u'KICT', u'KICX', u'KILN', u'KILX', u'KIND', u'KINX', u'KIWA', u'KIWX', u'KJAX', u'KJGX', u'KJKL', u'KLBB', u'KLCH', u'KLGX', u'KLIX', u'KLNX', u'KLOT', u'KLRX', u'KLSX', u'KLTX', u'KLVX', u'KLWX', u'KLZK', u'KMAF', u'KMAX', u'KMBX', u'KMHX', u'KMKX', u'KMLB', u'KMOB', u'KMPX', u'KMQT', u'KMRX', u'KMSX', u'KMTX', u'KMUX', u'KMVX', u'KMXX', u'KNKX', u'KNQA', u'KOAX', u'KOHX', u'KOKX', u'KOTX', u'KPAH', u'KPBZ', u'KPDT', u'KPOE', u'KPUX', u'KRAX', u'KRGX', u'KRIW', u'KRLX', u'KRTX', u'KSFX', u'KSGF', u'KSHV', u'KSJT', u'KSOX', u'KSRX', u'KTBW', u'KTFX', u'KTLH', u'KTLX', u'KTWX', u'KTYX', u'KUDX', u'KUEX', u'KVNX', u'KVTX', u'KVWX', u'KYUX', u'PHKI', u'PHKM', u'PHMO', u'PHWA', u'TJUA']

        :param year: the year we are requesting available radars for (i.e 2010)
        :type year: str
        :param month: the month we are requesting available radars for (i.e. 05)
        :type month: str
        :param day: the day we are requesting available radars for (i.e. 01)
        :type day: str
        :return: A list of string representing the radar sites available in the given day, month, and year
        :rtype list:

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

    def get_avail_scans(self, year, month, day, radar):
        """
        This method allows you to get the available radar scans for a given year, month, day, and radar.

        >>> print conn.get_avail_scans('2013','05','31','KTLX')
        >>> [AwsNexradFile object - 2013/05/31/KTLX/KTLX20130531_000358_V06.gz, AwsNexradFile object - 2013/05/31/KTLX/KTLX20130531_000834_V06.gz, AwsNexradFile object - 2013/05/31/KTLX/KTLX20130531_001311_V06.gz,...

        :param year: the year we are requesting available scans for (i.e 2010)
        :type year: str
        :param month: the month we are requesting available scans for (i.e. 05)
        :type month: str
        :param day: the day we are requesting available scans for (i.e. 01)
        :type day: str
        :param radar: the radar id we are requesting available scans for (i.e. KTLX)
        :type radar: str
        :return: A list of :class:`AwsNexradFile <nexradaws.resources.awsnexradfile.AwsNexradFile>` objects representing \
        the radar scans available for a given radar, day, month, and year
        :rtype list:

        """
        scans = []
        resp = self._bucket.meta.client.list_objects(Bucket='noaa-nexrad-level2',
                                                     Prefix='{}/{}/{}/{}/'.format(year,month,day,radar),
                                                     Delimiter='/')
        for scan in resp.get('Contents'):
            match = self._scan_re.match(scan.get('Key'))
            if match is not None:
                scans.append(AwsNexradFile(scan))
        return scans

    def get_avail_scans_in_range(self, start, end, radar):
        """
        Get all available scans for a radar between start and end date. \
        If datetime's do not include a timezone they will be set to UTC.

        >>> from datetime import datetime
        >>> radarid = 'KTLX'
        >>> start = datetime(2013, 5, 31, 20, 0)
        >>> end = datetime(2013, 5, 31, 23, 0)
        >>> print conn.get_avail_scans_in_range(start,end,radarid)
        >>> [AwsNexradFile object - 2013/05/31/KTLX/KTLX20130531_200046_V06.gz, AwsNexradFile object - 2013/05/31/KTLX/KTLX20130531_200415_V06.gz, AwsNexradFile object - 2013/05/31/KTLX/KTLX20130531_200745_V06.gz,...

        :param start: start time for range
        :type start: datetime
        :param end: end time for range
        :type end: datetime
        :param radar: radar id
        :type radar: str
        :return: A list of :class:`AwsNexradFile <nexradaws.resources.awsnexradfile.AwsNexradFile>` objects \
        representing the radar scans available in the passed time range.
        :rtype list:

        """
        scans = []
        utcstart,utcend = self._formattimerange(start,end)
        for day in self._datetime_range(utcstart,utcend):
            availscans = self.get_avail_scans('{0:0>2}'.format(day.year),
                                     '{0:0>2}'.format(day.month),
                                     '{0:0>2}'.format(day.day),
                                              radar.upper())
            for scan in availscans:
                if self._is_within_range(utcstart,utcend,scan.scan_time):
                    scans.append(scan)
        return scans

    def download(self, awsnexradfiles, basepath, keep_aws_folders=False, threads=6):
        """
        This method will download the passed AwsNexradFile object(s) to the given basepath folder.
        If keep_aws_folders is True then subfolders will be created under the basepath with the same
        structure as on AWS (year/month/day/radar/).

        :param awsnexradfiles: A list of :class:`AwsNexradFile <nexradaws.resources.awsnexradfile.AwsNexradFile>` objects to download
        :type awsnexradfiles: list
        :param basepath: location to save downloaded files
        :type basepath: str
        :param keep_aws_folders: weather or not to use the aws folder structure
         inside the basepath...(year/month/day/radar/)
        :type keep_aws_folders: bool
        :param threads: number of download threads to utilize (default=6)
        :type threads: int
        :return: A :class:`DownloadResults <nexradaws.resources.downloadresults.DownloadResults>` object that contains \
        successful downloads as :class:`LocalNexradFile <nexradaws.resources.localnexradfile.LocalNexradFile>` objects \
        as well as any :class:`AwsNexradFile <nexradaws.resources.awsnexradfile.AwsNexradFile>` objects that failed
        :rtype :class:`DownloadResults <nexradaws.resources.downloadresults.DownloadResults>`:

        """
        # If only a single AwsNexradFile object is passed convert to a list
        if type(awsnexradfiles) == AwsNexradFile:
            awsnexradfiles = [awsnexradfiles]
        localfiles = []
        errors = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_download = {executor.submit(self._download,nexradfile,basepath,keep_aws_folders): nexradfile for nexradfile in awsnexradfiles}
            for future in concurrent.futures.as_completed(future_download):
                try:
                    result = future.result()
                    localfiles.append(result)
                    six.print_("Downloaded {}".format(result.filename))
                except NexradAwsDownloadError:
                    error = future.exception()
                    errors.append(error.awsnexradfile)
        # Sort returned list of NexradLocalFile objects by the scan_time
        localfiles.sort(key=lambda x:x.scan_time)
        downloadresults = DownloadResults(localfiles,errors)
        six.print_('{} out of {} files downloaded...{} errors'.format(downloadresults.success_count,
                                                                      downloadresults.total,
                                                                      downloadresults.failed_count))
        return downloadresults

    def _download(self,awsnexradfile,basepath,keep_aws_folders):
        dirpath, filepath = awsnexradfile.create_filepath(basepath, keep_aws_folders)
        try:
            os.makedirs(dirpath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirpath):
                pass
            else:
                raise

        try:
            s3 = boto3.client('s3')
            s3.meta.events.register('choose-signer.s3.*', disable_signing)
            s3.download_file('noaa-nexrad-level2',awsnexradfile.key,filepath)
            return LocalNexradFile(awsnexradfile, filepath)
        except:
            message = 'Download failed for {}'.format(awsnexradfile.filename)
            raise NexradAwsDownloadError(message,awsnexradfile)

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

class NexradAwsDownloadError(Exception):
    def __init__(self,message,awsnexradfile):
        super(NexradAwsDownloadError, self).__init__(message)
        self.awsnexradfile = awsnexradfile
