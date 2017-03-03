import os
import sys
from subprocess import check_output
from settings import *
from shutil import copyfile

if not os.path.exists(out_folder):
    os.makedirs(out_folder)
for folder in folders:
	if not folder.endswith('/'):
		folder = folder+'/'
	print folder
	g = check_output('ls '+folder+' | grep -e Bus_GPS',shell = True)[0:-1]
	s = check_output('ls '+folder+' | grep -e Bus_S',shell = True)[0:-1]
	w = check_output('ls '+folder+' | grep -e Bus_W',shell = True)[0:-1]

	print g,s,w

	os.system('python sound_data_merge.py '+ s + ' ' + folder)
	os.system('python nemo.py '+ g+' op_'+s+' '+w+' '+ 'op' +' '+ folder)

	copyfile(folder.replace('\ ',' ')+'op',out_folder+folder.replace('/','_').replace('.','_'))
	
os.system('python launcher.py '+out_folder)
