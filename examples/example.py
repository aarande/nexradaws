import six
import nexradaws
conn = nexradaws.NexradAwsInterface()
six.print_(conn.get_avail_years())
six.print_(conn.get_avail_months('2013'))
six.print_(conn.get_avail_days('2013', '05'))
six.print_(conn.get_avail_radars('2013', '05', '31'))
six.print_(conn.get_avail_scans('2013', '05', '31', 'KTLX'))

from datetime import datetime
radarid = 'KTLX'
start = datetime(2013,5,31,20,00)
end = datetime(2013,5,31,23,00)
six.print_(conn.get_avail_scans_in_range(start, end, radarid))