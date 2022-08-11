#!/bin/bash

export OMPI_MCA_btl="tcp,self"
flux mini run -n 4 /var/flux/hello 2>/dev/null | grep -v Unable

