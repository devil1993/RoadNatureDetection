import sys
import numpy as np

folder=''
try:
	folder = sys.argv[2]
except Exception,e:
	print e
file = open(folder+sys.argv[1],'r')
lines = file.read().split('\n')
file.close()

op_file = open(folder+'op_'+sys.argv[1],'w')
i=0
try:
	while i < len(lines):
		#print i
		count = 1
		data = lines[i].split(',')
		_sum = float(data[1])
		next_data = lines[i+count].split(',')
		#print data[0][:-4],next_data[0][:-4]
		while(data[0][:-4] == next_data[0][:-4]):
			newData = float(next_data[1])
			if newData > _sum:
				_sum = newData
			count = count + 1
			next_data = lines[i+count].split(',')
			#print next_data
		op_file.write(data[0][11:-4]+','+str(_sum)+',0'+'\n')
		i = i+count
except Exception,e:
	print e
op_file.close()
