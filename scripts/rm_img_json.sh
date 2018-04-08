#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 [ first file number ] [ last file number ]"
    exit 1
fi

let n=$1
let m=$2

while [ $n -le $m ]; do
    rm ${n}_cam-image_array_.jpg record_${n}.json
    echo "rm ${n}_cam-image_array_.jpg record_${n}.json"

    let n=${n}+1
done
