#!/bin/bash

# configurable parameters

attr=(
cam/image_array
# cam_back/image_array
ultrasonic_front/distance
ultrasonic_front_left/distance
ultrasonic_front_right/distance
# ultrasonic_back/distance
# ultrasonic_back_left/distance
# ultrasonic_back_right/distance
ultrasonic_right/distance
ultrasonic_left/distance
user/mode
user/throttle
user/angle
)

#-----------------------------------------------------------------------
Usage()
{
    echo $*
    echo "Usage: $0 [ directory to store output ]"
    exit 1
}

if [ $# -lt 1 ]; then
    Usage "No directory specified"
else
    dir=$1
fi
if [ -f ${dir} ]; then
    Usage "Invalid directory ${dir}"
else
    if [ ! -d ${dir} ]; then
        mkdir ${dir}
    fi
fi

#-----------------------------------------------------------------------

a=`echo ${attr[@]} | tr ' ' '|'`
for fname in `ls -1 record_*.json`; do

    if [ -f ${fname} ]; then

        echo ${fname}
        record="{ `sed -e 's/, /\n/g' -e 's/{/{\n/g' -e 's/}/\n}/' ${fname} | egrep "${a}" | sed -e 's/$/,/'` }"
        echo ${record} | sed -e 's/, }/ }/' > ${dir}/${fname}

    else
        echo "${fname} not found"
    fi
done

echo "***** IMPORTANT: Remember to change meta.json as well *****"

exit 0
