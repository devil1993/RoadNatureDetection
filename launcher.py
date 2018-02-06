import os
import sys
from extractData import *

source_directory = sys.argv[sys.argv.index('-i')+1]
out_directory = sys.argv[sys.argv.index('-o')+1]
stopfile = sys.argv[sys.argv.index('-s')+1]

if not out_directory.endswith('/'):
	out_directory += '/'
if not source_directory.endswith('/'):
	source_directory += '/'
files = os.listdir(source_directory)

initialize_multi(source_directory,stopfile,out_directory)

if not os.path.exists(out_directory):
    os.makedirs(out_directory)

for file in files:
	pid = os.fork()
	if pid == 0:
		getInfo(file)
		print(file,"done")
		os._exit(0)
	else:
		print(pid,"working on file",file)