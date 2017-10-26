import os
import sys
from subprocess import check_output
from shutil import copyfile
from file_selector_settings import *

folders = check_output('ls ' + input_folder,shell = True).split('\n')

if not input_folder.endswith('/'):
	input_folder = input_folder+'/'

for folder in folders:
	print 'Folder:',folder
	if ' ' in folder:
		folder.replace(' ','\ ')
	#folder = folder.replace(' ','\ ')
	if(len(folder.split('.'))<=1):
		inner_folders = check_output('ls ' + input_folder + folder,shell = True).split('\n')
		for inner_folder in inner_folders:
			print 'Inner_folder:', inner_folder
			#inner_folder = inner_folder.replace(' ','\ ')
			if (len(inner_folder.split('.'))<=1):
				if not os.path.exists(input_folder + folder+'/'+inner_folder+'/selected_sensor_files'):
    					os.makedirs(input_folder + folder+'/'+inner_folder+'/selected_sensor_files')
				last_folders = check_output('ls ' + input_folder.replace(' ','\ ')+ folder.replace(' ','\ ')+'/'+inner_folder.replace(' ','\ '),shell = True).split('\n')
				for last_folder in last_folders:
					print 'Last folder: ',last_folder
					#last_folder = last_folder.replace(' ','\ ')
					if (len(last_folder.split('.'))<=1):
						for file_selector in file_selectors:
							try:
								file_names = check_output('ls '+input_folder.replace(' ','\ ')+folder.replace(' ','\ ')+'/'+inner_folder.replace(' ','\ ')+'/'+last_folder.replace(' ','\ ')+' | grep -e '+file_selector,shell= True).split('\n')
								for file_name in file_names:
									print 'File Name:', file_name
									if(len(file_name)==0):
										continue
									copyfile((input_folder+folder+'/'+inner_folder+'/'+last_folder+'/')+file_name,(input_folder + folder+'/'+inner_folder+'/selected_sensor_files/')+file_name)
							except Exception, e:
								pass