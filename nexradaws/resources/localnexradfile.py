import os
try:
    import pyart
    pyart_avail = True
except ImportError:
    pyart_avail = False

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

    def open_pyart(self):
        """
        If pyart is available this method will read in the nexrad archive file and return a \
        pyart Radar object.
        :return: a pyart radar object
        :rtype pyart.core.Radar:
        """
        if pyart_avail:
            return pyart.io.read_nexrad_archive(self.filepath)


