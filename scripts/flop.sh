#!/bin/bash

#-----------------------------------------------------------------------

Usage()
{
    echo $*
    echo "Usage: $0 [ original file number ] [ new file number ] [ number of files ]"
    exit 1
}

if [ $# -lt 2 ]; then
    Usage "No original and new file numbers specified"
else
    let orifno=$1
    let newfno=$2
fi

if [ $# -lt 3 ]; then
    Usage "number of files not specified"
else
    nfiles=$3
fi

#-----------------------------------------------------------------------

let n=${orifno}
let m=${newfno}
let lastfno=${orifno}+${nfiles}-1

while [ ${n} -le ${lastfno} ]; do

    ofname=${n}_cam-image_array_.jpg
    if [ -f ${ofname} ]; then

        nfname=${m}_cam-image_array_.jpg
        cp -p ${ofname} ${nfname}

        echo "gm mogrify -flop ${nfname}"
        gm mogrify -flop ${nfname}

    else
        echo "${ofname} not found"
    fi

    let n=${n}+1
    let m=${m}+1
done

#-----------------------------------------------------------

let n=${orifno}
let m=${newfno}
let lastfno=${orifno}+${nfiles}-1

while [ ${n} -le ${lastfno} ]; do

    ofname=${n}_cam_back-image_array_.jpg
    if [ -f ${ofname} ]; then

        nfname=${m}_cam_back-image_array_.jpg
        cp -p ${ofname} ${nfname}

        echo "gm mogrify -flop ${nfname}"
        gm mogrify -flop ${nfname}

    else
        echo "${ofname} not found"
    fi

    let n=${n}+1
    let m=${m}+1
done

#-----------------------------------------------------------

let n=${orifno}
let m=${newfno}
let lastfno=${orifno}+${nfiles}-1

while [ ${n} -le ${lastfno} ]; do

    ofname=record_${n}.json
    if [ -f ${ofname} ]; then

        nfname=record_${m}.json
        echo "cp -p ${ofname} ${nfname}"
        cp -p ${ofname} ${nfname}

    else
        echo "${ofname} not found"
    fi

    let n=${n}+1
    let m=${m}+1
done

exit 0
