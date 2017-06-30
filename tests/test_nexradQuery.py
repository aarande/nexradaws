from unittest import TestCase

from nexradaws.query import NexradQuery

examplemonths = ['{0:0>2}'.format(x) for x in range(1,13)]

exampledays = ['{0:0>2}'.format(x) for x in range(1,32)]
exampledaysleapyear = ['{0:0>2}'.format(x) for x in range(1,30)]

class TestNexradQuery(TestCase):
    def setUp(self):
        self.query = NexradQuery()

    def test_get_available_years(self):
        years = self.query.get_available_years()
        self.assertIsInstance(years,list)

    def test_get_available_months(self):
        months = self.query.get_available_months('2006')
        self.assertIsInstance(months,list)
        self.assertEqual(months, examplemonths)
        self.assertEqual(12,len(months))

    def test_get_available_days(self):
        days = self.query.get_available_days('2006','05')
        self.assertIsInstance(days,list)
        self.assertEqual(31,len(days))
        self.assertEqual(days,exampledays)

    def test_get_available_radars(self):
        radars = self.query.get_available_radars('2006','05','31')
        self.assertIsInstance(radars,list)
        self.assertTrue('KTLX' in radars)

