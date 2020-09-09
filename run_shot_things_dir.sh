#!/bin/bash

data=$1  # root dir of clusters or shots
outdir=${data}_person

# do video shot person detection, determine far/full/detail etc
for i in `ls $data`;do   
    echo $i
    if [ -d ${data}/${i} ]; then
        python detect_person_shot.py --save-txt --source ${data}/${i}  --output ${outdir}/${i}

    fi

done
