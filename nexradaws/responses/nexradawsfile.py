import os
import re

from datetime import datetime
import pytz


class NexradAwsFile(object):
    def __init__(self,scandict):
        self._scan_time_re = re.compile('(....)(\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2})_.*')
        self.key = scandict.get('Key',None)
        self.last_modified = scandict.get('LastModified',None)
        self.awspath = None
        self.filename = None
        self.scan_time = None
        self.radar_id = None
        if self.key is not None:
            self.parse_key()

    def parse_key(self):
        self.awspath,self.filename = os.path.split(self.key)
        match = self._scan_time_re.match(self.filename)
        if match is not None:
            self.radar_id = match.group(1)
            timestring = match.group(2)
            self.scan_time = datetime.strptime(timestring,
                                               '%Y%m%d_%H%M%S').replace(tzinfo=pytz.UTC)




