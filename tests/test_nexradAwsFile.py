from datetime import datetime
from unittest import TestCase

import pytz

import nexradaws


class TestNexradAwsFile(TestCase):
    def setUp(self):
        query = nexradaws.NexradAwsInterface()
        self.test_scan = query.get_avail_scans('2013', '05', '31', 'KTLX')[0]

    def test_parse_radarid(self):
        self.assertEqual(self.test_scan.radar_id, 'KTLX')

    def test_filename(self):
        self.assertEqual(self.test_scan.filename, u'KTLX20130531_000358_V06.gz')

    def test_scan_time(self):
        testdate = datetime(2013, 5, 31, 0, 3, 58, tzinfo=pytz.UTC)
        self.assertIsInstance(self.test_scan.scan_time, datetime)
        self.assertEqual(self.test_scan.scan_time, testdate)

    def test_key(self):
        self.assertEqual(self.test_scan.key, u'2013/05/31/KTLX/KTLX20130531_000358_V06.gz')
