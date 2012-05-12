@echo off
cd C:\WebShots\Worker
C:\WebShots\Python27\Scripts\celeryd.exe -Q updating,winxp_ff_3.6,winxp_op_10.10,winxp_ie_7 --concurrency=1 --maxtasksperchild=1 --time-limit=60 --hostname=winxp_2 -E --autoreload --loglevel=INFO --logfile=logWorker.log 