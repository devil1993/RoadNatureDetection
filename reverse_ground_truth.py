#! /usr/bin/python
import sys;

file = open(sys.argv[1],'r');
data = file.read().split('\n')
file.close();

file = open('reverse_' + sys.argv[1],'w')

data.reverse()

for datum in data:
	file.write(datum+'\n')

file.close()