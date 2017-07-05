import tempfile
from unittest import TestCase

from datetime import datetime

import shutil

import nexradaws
from nexradaws.resources.localnexradfile import LocalNexradFile
from nexradaws.resources.nexradawsfile import NexradAwsFile


class TestDownloadResults(TestCase):
    def setUp(self):
        self.query = nexradaws.NexradAwsInterface()
        self.templocation = tempfile.mkdtemp()
        start = datetime(2013, 5, 20, 18, 45)
        end = datetime(2013, 5, 20, 19, 00)
        self.scans = self.query.get_avail_scans_in_range(start, end, 'KTLX')

    def tearDown(self):
        shutil.rmtree(self.templocation)

    def test_total(self):
        results = self.query.download(self.scans,self.templocation)
        self.assertEqual(len(self.scans),results.total)

    def test_success_count(self):
        results = self.query.download(self.scans, self.templocation)
        self.assertEqual(results.success_count,len(self.scans))

    def test_failed_count(self):
        self.scans[0].key = 'blah/blah'
        results = self.query.download(self.scans, self.templocation)
        self.assertEqual(results.failed_count,1)

    def test_success(self):
        results = self.query.download(self.scans, self.templocation)
        self.assertIsInstance(results.success,list)
        self.assertIsInstance(results.success[0],LocalNexradFile)

    def test_failed(self):
        # Change the key to the first scan to enduce a download failure
        self.scans[0].key = 'blah/blah'
        results = self.query.download(self.scans, self.templocation)
        self.assertIsInstance(results.failed,list)

    def test_iter_success(self):
        results = self.query.download(self.scans, self.templocation)
        for localfile in results.iter_success():
            self.assertIsInstance(localfile,LocalNexradFile)

    def test_iter_failed(self):
        # Change the key to the first scan to enduce a download failure
        self.scans[0].key = 'blah/blah'
        results = self.query.download(self.scans, self.templocation)
        for errorfile in results.iter_failed():
            self.assertIsInstance(errorfile,NexradAwsFile)
