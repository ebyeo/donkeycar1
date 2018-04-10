#!/bin/bash

# configurable parameters
PARAM=throttle
POS=8

#-----------------------------------------------------------------------

Usage()
{
    echo $*
    echo "Usage: $0 [ start file number ] [ end file number ] [ value ] [ flop start file number ]"
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

if [ $# -ge 4 ]; then
    flopfno=$4
    let flop=1
else
    let flop=0
fi

#-----------------------------------------------------------------------

let n=${firstfno}
let m=${lastfno}

while [ ${n} -le ${m} ]; do
    fname=record_${n}.json
    if [ -f ${fname} ]; then

        echo ${fname}
        sed -e 's/,/,\n/g' ${fname} | \
        awk -F: -v par="${PARAM}" -v pos="${POS}" -v v="${val}"\
            '{if(substr($0,pos,length(par))==par) {sub($2,v); printf $0","} else printf $0}' > ${fname}_new
        mv ${fname}_new ${fname}

    else
        echo "${fname} not found"
    fi

    let n=${n}+1
done

#-----------------------------------------------------------------------

if [ ${flop} -eq 1 ]; then
let n=${flopfno}
let m=${n}+${lastfno}-${firstfno}

let f1=${firstfno}

while [ ${n} -le ${m} ]; do
    fname=record_${n}.json
    if [ -f ${fname} ]; then

        echo ${fname}
        sed -e 's/,/,\n/g' ${fname} | \
        awk -F: -v par="${PARAM}" -v pos="${POS}" -v v="${val}"\
            '{if(substr($0,pos,length(par))==par) {sub($2,v); printf $0","} else printf $0}' | \
        awk -v f1="${f1}_" -v f2="${n}_" '{gsub(f1,f2); printf $0}' \
        > ${fname}_new

        mv ${fname}_new ${fname}

    else
        echo "${fname} not found"
    fi

    let n=${n}+1
    let f1=${f1}+1
done
fi

exit 0
