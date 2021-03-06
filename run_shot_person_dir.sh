#!/bin/bash

data=$1  # root dir of clusters or shots
outdir=${data}_person
outimgdir=${data}_person_dropshot

:<<EOF
# do video shot person detection, determine far/full/detail etc
for i in `ls $data`;do   
    echo $i
    if [ -d ${data}/${i} ]; then
        python detect_person.py --save-txt --source ${data}/${i}  --output ${outdir}/${i}

    fi

done
EOF
python get_shot_nonperson_imgdir.py ${outdir} ${data} ${outimgdir}