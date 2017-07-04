class DownloadResults(object):
    def __init__(self,localfiles,failedfiles):
        super(DownloadResults, self).__init__()
        self._successfiles = localfiles
        self._failedfiles = failedfiles

    @property
    def failed_count(self):
        return len(self._failedfiles)

    @property
    def success_count(self):
        return len(self._successfiles)

    @property
    def total(self):
        return self.success_count + self.failed_count

    @property
    def success(self):
        return self._successfiles

    @property
    def failed(self):
        return self._failedfiles

    def iter_success(self):
        for nexradfile in self.success:
            yield nexradfile

    def iter_failed(self):
        for nexradawsfile in self.failed:
            yield nexradawsfile


