__author__ = 'Aaron Anderson'

import boto
import re

class NexradQuery(object):
    def __init__(self, aws_access_key, aws_secret_access_key):
        self.year_re = re.compile('^(\d{4})/')
        self.month_re = re.compile('^\d{4}/(\d{2})')
        self.day_re = re.compile('^\d{4}/\d{2}/(\d{2})')
        self.radar_re = re.compile('^\d{4}/\d{2}/\d{2}/(....)/')
        self.s3conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
        self.bucket = self.s3conn.get_bucket('noaa-nexrad-level2')

    def get_available_years(self):
        years = []
        resp = list(self.bucket.list("","/"))
        for each in resp:
            match = self.year_re.match(each.name)
            if match != None:
            #TODO regex to strip out anything other than a year
                years.append(match.group(1))
        return years

    def get_available_months(self,year):
        months = []
        resp = list(self.bucket.list("%s/"%year,"/"))
        for each in resp:
            match = self.month_re.match(each.name)
            if match != None:
                months.append(match.group(1))
        return months

    def get_available_days(self,year,month):
        days = []
        resp = list(self.bucket.list("%s/%s/"%(year,month),"/"))
        for each in resp:
            match = self.day_re.match(each.name)
            if match != None:
                days.append(match.group(1))
        return days

    def get_available_radars(self,year,month,day):
        radars = []
        resp = list(self.bucket.list("%s/%s/%s/"%(year,month,day),"/"))
        for each in resp:
            match = self.radar_re.match(each.name)
            if match != None:
                radars.append(match.group(1))
        return radars

if __name__ == '__main__':
    import testvalues
    query = NexradQuery(testvalues.aws_access_key,testvalues.aws_secret_access_key)
    print query.get_available_years()
    print query.get_available_months("2010")
    print query.get_available_days("2010","02")
    print query.get_available_radars("2010","02","02")