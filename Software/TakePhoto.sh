#!/bin/bash

python3 ${dir}/SetPin.py 8
raspistill --mode 4 --nopreview --output ${dir}/last.jpg
python3 ${dir}/SetPin.py -8
