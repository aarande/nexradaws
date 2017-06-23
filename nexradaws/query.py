__author__ = 'Aaron Anderson'

from boto.s3.connection import S3Connection
import re

class NexradQuery(object):
    def __init__(self):
        self.year_re = re.compile('^(\d{4})/')
        self.month_re = re.compile('^\d{4}/(\d{2})')
        self.day_re = re.compile('^\d{4}/\d{2}/(\d{2})')
        self.radar_re = re.compile('^\d{4}/\d{2}/\d{2}/(....)/')
        self.scan_re = re.compile('^\d{4}/\d{2}/\d{2}/..../(.*.gz)')
        self.s3conn = S3Connection(anon=True)
        self.bucket = self.s3conn.get_bucket('noaa-nexrad-level2')

    def get_available_years(self):
        """
        This method allows you to get the years that are currently available.
        :rtype : list
        :return: A list of strings representing the years available
        """
        years = []
        resp = list(self.bucket.list("","/"))
        for each in resp:
            match = self.year_re.match(each.name)
            if match != None:
                years.append(match.group(1))
        return years

    def get_available_months(self,year):
        """
        This method allows you to get the available months in a given year.
        :rtype : list
        :param year: string - the year we are requesting available months for (i.e. 2010)
        :return: A list of strings representing the months available for that year
        """
        months = []
        resp = list(self.bucket.list("%s/"%year,"/"))
        for each in resp:
            match = self.month_re.match(each.name)
            if match != None:
                months.append(match.group(1))
        return months

    def get_available_days(self,year,month):
        """
        This method allows you to get the available days in a given month and year.
        :rtype : list
        :param year: string - the year we are requesting available days for (i.e 2010)
        :param month: string - the month we are requesting available days for (i.e. 05)
        :return: A list of strings representing the days available in the given month and year
        """
        days = []
        resp = list(self.bucket.list("%s/%s/"%(year,month),"/"))
        for each in resp:
            match = self.day_re.match(each.name)
            if match != None:
                days.append(match.group(1))
        return days

    def get_available_radars(self,year,month,day):
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
        resp = list(self.bucket.list("%s/%s/%s/"%(year,month,day),"/"))
        for each in resp:
            match = self.radar_re.match(each.name)
            if match != None:
                radars.append(match.group(1))
        return radars

    def get_available_scans(self,year,month,day,radar):
        """
        This method allows you to get the available radar scans for a given radar, day, month, and year.
        :rtype : list
        :param year: string - the year we are requesting available scans for (i.e 2010)
        :param month: string - the month we are requesting available scans for (i.e. 05)
        :param day: string - the day we are requesting available scans for (i.e. 01)
        :param radar: string - the radar id we are requesting available scans for (i.e. KTLX)
        :return: A list of string representing the radar scans available for a given radar,
        day, month, and year
        """
        scans = []
        resp = list(self.bucket.list("%s/%s/%s/%s/" % (year, month, day,radar)))
        for each in resp:
            match = self.scan_re.match(each.name)
            if match != None:
                scans.append(match.group(1))
        return scans


if __name__ == '__main__':
    query = NexradQuery()
    print query.get_available_years()
    print query.get_available_months("2010")
    print query.get_available_days("2010","02")
    print query.get_available_radars("2010","02","02")
    print query.get_available_scans("2010","02","02","KTLX")