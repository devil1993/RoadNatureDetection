import os
import sys
from subprocess import check_output
from settings import *
from shutil import copyfile

if '-help' in sys.argv:
	print('-f','Folder path')
	print('-o','Output folder path')
	print('-s','Stops file')
	print('-p','Output file prefix')
	print('-help','HELP')
	quit()

if '-f' in sys.argv:
	index = sys.argv.index('-f') + 1
	folders = [sys.argv[index]]
	folder = folders[0]

if '-o' in sys.argv:
	index = sys.argv.index('-o') + 1
	out_folder = [sys.argv[index]]

if '-s' in sys.argv:
	index = sys.argv.index('-s') + 1
	config['ground_truth_file'] = [sys.argv[index]]
	stopfiile = [sys.argv[index]]

if '-p' in sys.argv:
	index = sys.argv.index('-p') + 1
	config['output_file_prefix'] = [sys.argv[index]]

'''
for folder in folders:
	try:
		if not folder.endswith('/'):
			folder = folder+'/'
		print(folder)
		os.system('rm -r '+folder+'tags')
		os.system('rm '+folder+'op*')
		g = check_output('ls '+folder+' | grep -e Scooty_GPS',shell = True)[0:-1].decode()
		s = check_output('ls '+folder+' | grep -e Scooty_S',shell = True)[0:-1].decode()
		w = check_output('ls '+folder+' | grep -e Scooty_W',shell = True)[0:-1].decode()

		print(g,s,w)

		os.system('python sound_data_merge.py '+ s + ' ' + folder)
		os.system('python nemo.py '+ g+' op_'+s+' '+w+' '+ 'op' +' '+ folder)
		if not os.path.exists(out_folder):
			os.makedirs(out_folder)
		copyfile(folder.replace('\ ',' ')+'op',out_folder+folder.replace('/','_').replace('.','_'))
		os.system('rm '+folder.replace('\ ',' ')+'op*')

		os.system('python rating_merge.py '+ folder+'tags/Busy_Road/ '+folder+'Bus_Rating.txt')
	except Exception as e:
		print(e)

'''

os.system('python launcher.py -i '+folder+' -o '+out_folder + ' -s '+ stopfiile)
print("===============================================DONE========================================================================")
