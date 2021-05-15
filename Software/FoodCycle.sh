#!/bin/bash

dir=/home/pi/CatFeeder
export BlobUploadUrl="https://homecv.blob.core.windows.net/"
export BlobUploadSas=`cat ${dir}/BlobUploadSas`

python3 ${dir}/SetPin.py 8

# see https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
# --output if - then stdout

#Mode	Size	    Aspect Ratio	Frame rates	FOV	Binning
#0      automatic selection				
#1      1920x1080	16:9	0.1-30fps	Partial	None
#2      3280x2464	4:3	    0.1-15fps	Full	None
#3      3280x2464	4:3	    0.1-15fps	Full	None
#4      1640x1232	4:3	    0.1-40fps	Full	2x2
#5      1640x922	16:9	0.1-40fps	Full	2x2
#6      1280x720	16:9	40-90fps	Partial	2x2
#7      640x480	    4:3	    40-200fps1	Partial	2x2

#raspivid --timeout 5000 --mode 4 --nopreview --output - && python3 ${dir}/SetPin.py -8 | python3 ${dir}/BlobUpload.py &
#raspivid --timeout 30000 --mode 4 --nopreview --output - | python3 ${dir}/BlobUpload.py &
(raspivid --timeout 30000 --mode 4 --nopreview --output ${dir}/last.h264 && MP4Box -fps 30 -add ${dir}/last.h264 ${dir}/last.mp4 && cat ${dir}/last.mp4 | python3 ${dir}/BlobUpload.py > ${dir}/last.log)&

${dir}/CatFeeder
date >> ${dir}/timestamp.log
sleep 60
python3 ${dir}/SetPin.py -8
