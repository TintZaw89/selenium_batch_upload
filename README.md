Batch Balance Adjust || Batch Recharge

--version 1.0 (Put all files together inside a folder)
P.S. This automation process has buggy and not stable :P. Use it with your own risk.

Model_ini.txt >> config parameter for batch upload file. Process will read first line of file to get data.
------------
column1=filename
column2=Recharge(R) or Adjustment(A)
column3=Credit, deduct for adjustment
column4=lines_per_file (to cut line per file)
coulmn5= to check column name (1) or to operate (0)
coulmn6=T for testbed, P for production
coulmn7=username
column8=password (optional if not have input data, need to fill at runtime)
culumn9=sec_per_batch to upload per file
column10=export log file (1=true,0=false)
column11=prefer browser(F for Firefox, C for Chrome, E for Edge and S for Safari.)
------------
py.bat >> to run python file in window terminal
-Replace "C:\Python312\python.exe" with your local python executable path
-Replace "C:\Users\BatchUpload\batch_upload_tz.py" with your python file full path (e.g C:\Users\Your_Path\batch_upload_tz.py)
------------
Package to install
------------
Install Python 
python get-pip.py
pip install selenium
pip install maskpass
pip list
