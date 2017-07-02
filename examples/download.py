import nexradaws
import tempfile
templocation = tempfile.mkdtemp()
conn = nexradaws.NexradAwsInterface()
scans = conn.get_available_scans('2013','05','31','KTLX')

localfiles = conn.download(scans[0],templocation)
print localfiles
print localfiles[0].filepath