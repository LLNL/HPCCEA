#!/bin/bash

## Simple guest creation script
## Reads creation parameters from guest_params.txt

# Path for guest_params.txt. Overridden if $1 exists as an alternate path.
if [ $# -gt 0 ]; then
	params=$1
else
	params=/root/kvm_project/guest_params.txt  # Change as necessary
fi

# Read and parse parameters from file
while IFS= read -r line; do
	param_name=$(echo "$line" | cut -d"=" -f 1)
	param_val=$(echo "$line" | cut -d"=" -f 1 --complement)
	eval $param_name=\$param_val
done < "$params"

# Create the guest

if [ "$graphics" = "nographics" ]; then
        virt-install \
        --name "$name" \
        --ram "$ram" \
        --vcpus="$vcpus" \
        --os-variant="$os_variant" \
        --nographics \
        --disk path="$disk_path",size="$disk_size",bus="$disk_bus",format="$disk_format" \
        --network "$network" \
        --location="$location" \
        --extra-args $extra_args  # Note: in the params file, make sure each extra arg is in ""
fi
