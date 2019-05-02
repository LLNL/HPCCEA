# script which runs the oscap command for RHEL7
# prints out one line to stdout of pass/fail/other counter
# sends fail ID's to fail.txt and syslog
# written by Alicja Gornicka

import subprocess
import sys
import socket
import syslog
import string

# runs oscap command for rhel7
test = subprocess.Popen(['/usr/bin/oscap', 'xccdf', 'eval', '--fetch-remote-resources', '--profile', 'xccdf_org.ssgproject.content_profile_stig-rhel7-disa', '--results', 'results.xml', '--report', 'report.html', '/usr/share/xml/scap/ssg/content/ssg-rhel7-ds.xml'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# counter variables for pass, fail, and other
passCount = 0
failCount = 0
other = 0 # notchecked and notapplicable

# colors for the output
GREEN = '\33[92m'
RED = '\33[91m'
LAVENDER = '\33[94m'
ORANGE = '\33[93m'
END = '\033[0m'

# opens fail.txt
fail = open("fail.txt",'wb')
fail.write("These are the failed rules.\n")
fail.write("To see more details, cp report.html /var/www/html/ and lynx http://boroni/report.html\n")
fail.write("\n" + socket.gethostname() + ":\n\n")

# grabs rule ID from stdout
# if rules failed, prints rule ID to fail.txt and syslog
for line in test.stdout:
  if "Rule" in line:
    rule = string.replace(line,'\r','') # needed to remove ^M characters from fail.txt
  if "Result" in line:
    if 'fail' in line:
      failCount += 1
      fail.write(rule)
      syslog.syslog(rule)
    elif 'pass' in line:
      passCount += 1
    elif 'notchecked' or 'notapplicable' in line:
      other += 1

# total number of rules checked
total = passCount + failCount + other

print (ORANGE + socket.gethostname() + END)  + ": " + (GREEN + "Pass count: " + END)  +  str(passCount) + "/" + str(total)  + (RED + "  Fail count: " + END) + str(failCount) + "/" + str(total) + (LAVENDER + "  Other count: " + END) + str(other) + "/" + str(total)

fail.close()
