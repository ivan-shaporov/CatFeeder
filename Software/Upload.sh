#!/bin/bash

ffmpeg -i ${dir}/last.h264 -c copy ${dir}/last.mp4 -y
ffmpeg -ss 00:00:02 -i ${dir}/last.mp4 -vframes 1 -vf "scale=640:480" ${dir}/last.jpg -y
python3 ${dir}/BlobUpload.py ${dir}/last >> ${dir}/upload.log 2>&1
