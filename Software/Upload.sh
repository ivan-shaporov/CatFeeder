#!/bin/bash

timestamp=`date +%s`

ffmpeg -i ${dir}/last.h264 ${dir}/last.mp4 -y
ffmpeg -ss 1.6 -i ${dir}/last.mp4 -vframes 1 -vf "scale=640:480" ${dir}/last.jpg -y
python3 ${dir}/BlobUpload.py -f ${dir}/last -t $timestamp >> ${dir}/upload.log 2>&1
