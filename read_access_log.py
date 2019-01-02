"""
Read Python Anywhere's access log file and figure out what IPs were on the site.
"""

from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
access_log_file = open("log_sample.txt", encoding='ISO-8859-1')

for a in range(0,5):
    b = access_log_file.readline()
    c = b.split('"')
    ip_address = c[7]
    url = c[3]
    d = c[0].split('[')
    e = d[1].split(']')[0]
    access_time = e.split()[0]
    #local_time = parse(access_time)
    local_time = datetime.strptime(access_time,'%d/%b/%Y:%H:%M:%S') - timedelta(hours=8)
    print(local_time.strftime('%b %-d %Y:%h:%M'), ip_address, url)