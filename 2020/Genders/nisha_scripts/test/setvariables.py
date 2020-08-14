# Test setting environment variables in python
# UPDATE -----------
# ERROR: doesn't work the same as exporting the variables in bash - create a driver script instead + debug
import os

os.environ['PYTHONPATH'] = '/usr/local/lib64/python3.6/site-packages'
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

print(os.environ.get('PYTHONPATH'))
print(os.environ.get('LD_LIBRARY_PATH'))

import genders
genders_object = genders.Genders(filename="/etc/genders")
print(genders_object.getattr())
