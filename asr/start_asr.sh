#!/bin/bash
source /agibot/data/home/agi/miniconda3/etc/profile.d/conda.sh
source /agibot/data/home/agi/.bashrc
conda activate base
echo "<<< start asr.py ! >>>"
# python3 asr.py >> output.txt
python3 asr.py 
