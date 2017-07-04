import os
import shutil
import tempfile
from unittest import TestCase

import pytz
import six
from datetime import datetime

import nexradaws
from nexradaws.resources.nexradawsfile import NexradAwsFile

examplemonths = ['{0:0>2}'.format(x) for x in range(1, 13)]

exampledays = ['{0:0>2}'.format(x) for x in range(1, 32)]
exampledaysleapyear = ['{0:0>2}'.format(x) for x in range(1, 30)]


class TestNexradAwsInterface(TestCase):
    def setUp(self):
        self.query = nexradaws.NexradAwsInterface()
        self.templocation = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.templocation)

    def test_get_available_years(self):
        years = self.query.get_available_years()
        self.assertIsInstance(years, list)

    def test_get_available_months(self):
        months = self.query.get_available_months('2006')
        self.assertIsInstance(months, list)
        six.assertCountEqual(self, months, examplemonths)
        self.assertEqual(12, len(months))

    def test_get_available_days(self):
        days = self.query.get_available_days('2006', '05')
        self.assertIsInstance(days, list)
        self.assertEqual(31, len(days))
        six.assertCountEqual(self, days, exampledays)

    def test_get_available_radars(self):
        radars = self.query.get_available_radars('2006', '05', '31')
        self.assertIsInstance(radars, list)
        self.assertTrue('KTLX' in radars)

    def test_get_available_scans(self):
        scans = self.query.get_available_scans('2006', '05', '31', 'KTLX')
        self.assertIsInstance(scans, list)

    def test_get_available_scans_in_range(self):
        start = datetime(2013, 5, 20, 18, 00)
        end = datetime(2013, 5, 20, 22, 00)
        scans = self.query.get_available_scans_in_range(start, end, 'KTLX')
        self.assertEqual(len(scans),53)
        self.assertIsInstance(scans[0],NexradAwsFile)

    def test_formattimerange_localtime(self):
        localtime = pytz.timezone('US/Central')
        start = localtime.localize(datetime(2013, 5, 20, 18, 00))
        end = localtime.localize(datetime(2013, 5, 20, 22, 00))
        utcstart,utcend = self.query._formattimerange(start,end)
        self.assertEqual(utcstart.tzinfo,pytz.UTC)
        self.assertEqual(utcend.tzinfo,pytz.UTC)

    def test_formattimerange_utc(self):
        localtime = pytz.UTC
        start = localtime.localize(datetime(2013, 5, 20, 18, 00))
        end = localtime.localize(datetime(2013, 5, 20, 22, 00))
        utcstart,utcend = self.query._formattimerange(start,end)
        self.assertEqual(utcstart.tzinfo,pytz.UTC)
        self.assertEqual(utcend.tzinfo,pytz.UTC)
        self.assertEqual(start,utcstart)
        self.assertEqual(end,utcend)

    def test_download_single(self):
        scans = self.query.get_available_scans('2006', '05', '31', 'KTLX')
        scan = scans[0]
        dirpath,filepath = scan.create_filepath(self.templocation,False)
        results = self.query.download(scan,self.templocation)
        self.assertTrue(os.path.isfile(filepath))
        self.assertEqual(results.failed_count,0)

    def test_download_multiple(self):
        scans = self.query.get_available_scans('2006', '05', '31', 'KTLX')
        multiplescans = scans[0:12]
        results = self.query.download(multiplescans, self.templocation)
        for scan in multiplescans:
            dirpath,filepath = scan.create_filepath(self.templocation,False)
            self.assertTrue(os.path.isfile(filepath))
        self.assertEqual(results.failed_count, 0)
