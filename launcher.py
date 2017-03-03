import os
import sys
from extractData import *

source_directory = sys.argv[1]
files = os.listdir(source_directory)

initialize_multi(source_directory)

if not os.path.exists(source_directory+'/results'):
    os.makedirs(source_directory+'/results')

for file in files:
	pid = os.fork()
	if pid == 0:
		getInfo(file)
		print file,"done"
		os._exit(0)
	else:
		print pid,"working on file",file