# script for converting jpg file into png file

import os,sys
folder = '/home/harshitw/Documents/Projects/CaptchaBreaker/downloads'
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename):
           continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.jpg', '.png')
       output = os.rename(infilename, newname)
