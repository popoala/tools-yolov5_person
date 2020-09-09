#!/bin/bash

data=$1  # root dir of clusters or shots
outdir=${data}_person
outimgdir=${data}_person_dropimg

:<<EOF
for i in `ls $data`;do  # for each class-dir
    echo $i
    if [ -d ${data}/${i} ]; then
        python detect_person.py --save-txt --classes 0 --source ${data}/${i}  --output ${outdir}/${i} --save-img --conf-thres 0.2

    fi

done
EOF

python get_class_nonperson_imgdir.py ${outdir} ${data} ${outimgdir}