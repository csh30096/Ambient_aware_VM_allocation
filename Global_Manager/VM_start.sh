#! bin/bash

#####################################
# $# - VM name list
#####################################

while [ $# -gt 0 ]
do
	virsh start $1
	shift
done

