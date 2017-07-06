import os

try:
    import pyart

    pyart_avail = True
except ImportError:
    pyart_avail = False


class LocalNexradFile(object):
    """
    This class contains metadata about the local NEXRAD file as well as methods to open the file.

    :var key: AWS key for this NEXRAD file
    :vartype key: str
    :var last_modified: when the file was last modified on AWS
    :vartype last_modified: datetime
    :var filename: the NEXRAD filename
    :vartype filename: str
    :var scan_time: volume scan time for the NEXRAD file
    :vartype scan_time: datetime
    :var radar_id: the four letter radar id (i.e. KTLX)
    :vartype radar_id: str
    :var filepath: absolute path to the downloaded file on the local system
    :vartype str:
    """
    def __init__(self, awsnexradfile, localfilepath):
        super(LocalNexradFile, self).__init__()
        self.key = awsnexradfile.key
        self.last_modified = awsnexradfile.last_modified
        self.filename = awsnexradfile.filename
        self.scan_time = awsnexradfile.scan_time
        self.radar_id = awsnexradfile.radar_id
        self.filepath = localfilepath

    def open(self):
        """
        Provides a file object to the local nexrad radar file. \
        Be sure to close the file object when processing is complete.

        :return: file object ready for reading
        :rtype file:
        """
        return open(self.filepath, 'rb')

    def open_pyart(self):
        """
        If pyart is available this method will read in the nexrad archive file and return a \
        pyart Radar object.

        :return: a pyart radar object
        :rtype pyart.core.Radar:
        """
        if pyart_avail:
            return pyart.io.read_nexrad_archive(self.filepath)
        else:
            raise ImportError("pyart module must be installed to use this function.")

    def __repr__(self):
        return '<LocalNexradFile object - {}>'.format(self.filepath)
