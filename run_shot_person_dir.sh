#!/bin/bash

data=$1  # root dir of clusters or shots
outdir=${data}_person
outimgdir=${data}_person_dropshot

# do video shot person detection, determine far/full/detail etc
for i in `ls $data`;do   
    echo $i
    if [ -d ${data}/${i} ]; then
        python detect_person_shot.py --save-txt --classes 0 --source ${data}/${i}  --output ${outdir}/${i}

    fi

done

python get_shot_nonperson_imgdir.py ${outdir} ${data} ${outimgdir}