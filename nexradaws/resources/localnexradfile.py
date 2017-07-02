import os

class LocalNexradFile(object):
    def __init__(self,nexradawsfile,localfilepath):
        self.key = nexradawsfile.key
        self.last_modified = nexradawsfile.last_modified
        self.filename = nexradawsfile.filename
        self.scan_time = nexradawsfile.scan_time
        self.radar_id = nexradawsfile.radar_id
        self.filepath = localfilepath

    def open(self):
        """
        Provides a file object to the local nexrad radar file. \
        Be sure to close the file object when processing is complete.
        :return: file object ready for reading
        :rtype file:
        """
        return open(self.filepath,'rb')
