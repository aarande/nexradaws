import os
import re

from datetime import datetime
import pytz


class NexradAwsFile(object):
    def __init__(self,scandict):
        self._scan_time_re = re.compile('(....)(\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}).*gz')
        self.key = scandict.get('Key',None)
        self.last_modified = scandict.get('LastModified',None)
        self.awspath = None
        self.filename = None
        self.scan_time = None
        self.radar_id = None
        if self.key is not None:
            self._parse_key()

    def _parse_key(self):
        self.awspath,self.filename = os.path.split(self.key)
        match = self._scan_time_re.match(self.filename)
        if match is not None:
            self.radar_id = match.group(1)
            timestring = match.group(2)
            self.scan_time = datetime.strptime(timestring,
                                               '%Y%m%d_%H%M%S').replace(tzinfo=pytz.UTC)

    def create_filepath(self, basepath, keep_aws_structure):
        """
        This function creates the file path in preperation for downloading. If keep_aws_structure
        is True then subfolders will be created under the basepath with the same structure as the
        AWS Nexrad Bucket.

        :param basepath: string - base folder to save files too
        :param keep_aws_structure: boolean - weather or not to use the aws folder structure
         inside the basepath...(year/month/day/radar/)
        :return: tuple - directory path and full filepath

        """
        if keep_aws_structure:
            directorypath = os.path.join(basepath,self.awspath)
            filepath = os.path.join(directorypath,self.filename)
        else:
            directorypath = basepath
            filepath = os.path.join(basepath, self.filename)

        return directorypath,filepath

    def __repr__(self):
        return 'NexradAwsFile object - {}'.format(self.key)




