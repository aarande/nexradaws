import nexradaws
conn = nexradaws.NexradAwsInterface()
print conn.get_avail_years()
print conn.get_avail_months('2013')
print conn.get_avail_days('2013', '05')
print conn.get_avail_radars('2013', '05', '31')
print conn.get_avail_scans('2013', '05', '31', 'KTLX')

from datetime import datetime
radarid = 'KTLX'
start = datetime(2013,5,31,20,00)
end = datetime(2013,5,31,23,00)
print conn.get_avail_scans_in_range(start, end, radarid)