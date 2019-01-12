"""
Read Python Anywhere's access log file and figure out what IPs were on the site.
"""

from datetime import datetime
from datetime import timedelta

import urllib.request
from collections import defaultdict
import urllib.request

from bs4 import BeautifulSoup
import requests
import lxml
import urllib.request

search_url = "https://www.pythonanywhere.com/user/daveperry10/files/var/log/www.positive-pets.org.access.log"

source = requests.get(search_url).text
soup = BeautifulSoup(source,'lxml')
print(soup.prettify())
#for txt in soup.find('pre'):
    #print(txt)



# access_log_file = open(txt)
#
# N = len(access_log_file.readlines())
# access_log_file.seek(0)
# for a in range(0, N):
#     b = access_log_file.readline()
#     c = b.split('"')
#     ip_address = c[7]
#     url = c[3]
#     try:
#         action = url.split("positivepets")[1]
#     except:
#         action = url
#     d = c[0].split('[')
#     e = d[1].split(']')[0]
#     access_time = e.split()[0]
#     local_time = datetime.strptime(access_time,'%d/%b/%Y:%H:%M:%S') - timedelta(hours=8)
#     if ip_address != "71.198.172.81":
#         print(local_time.strftime('%b %d, %I:%M'), ip_address, action)