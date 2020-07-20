import os

os.environ['PYTHONPATH'] = '/usr/local/lib64/python3.6/site-packages'
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

import genders
genders_object = genders.Genders(filename="/etc/genders")
print(genders_object.getattr())
