#!/bin/bash

# configurable parameters
PARAM=ultrasonic_right
POS=3

#-----------------------------------------------------------------------

Usage()
{
    echo $*
    echo "Usage: $0 [ start file number ] [ end file number ] [ value ]"
    exit 1
}

if [ $# -lt 2 ]; then
    Usage "No start and end file numbers specified"
else
    let firstfno=$1
    let lastfno=$2
fi

if [ $# -lt 3 ]; then
    Usage "No value specified"
else
    val=$3
fi

#-----------------------------------------------------------------------

let n=${firstfno}
while [ ${n} -le ${lastfno} ]; do
    fname=record_${n}.json
    if [ -f ${fname} ]; then

        sed -e 's/,/,\n/g' ${fname} | \
        awk -F: -v par="${PARAM}" -v pos="${POS}" -v v="${val}"\
            '{if(substr($0,pos,length(par))==par) {sub($2,v); printf $0","} else printf $0}' > ${fname}_new
        mv ${fname}_new ${fname}

    else
        echo "${fname} not found"
    fi

    let n=${n}+1
done

exit 0
