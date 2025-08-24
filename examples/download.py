import nexradaws
import tempfile
templocation = tempfile.mkdtemp()
conn = nexradaws.NexradAwsInterface()
scans = conn.get_avail_scans('2013', '05', '31', 'KTLX')

localfiles = conn.download(scans[0:12],templocation)
print(localfiles.success)
print(localfiles.success[0].filepath)