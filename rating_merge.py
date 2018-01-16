import numpy as np
import sys
from subprocess import check_output
import os 
datatype=np.dtype([('behave','a30'),('rate',int),('time','a30')])
busy_folder = sys.argv[1]
# '/media/rrocks/682C31EA2C31B3C2/project/Data/RoadSegmentBehaviourAnalysis/DataSet/ByAbhijit/Bus/Date_20_09_17ukhra/DATA_17_12_44/All/U_C/tags/Busy_Road/'
rating_file= sys.argv[2]
# '/media/rrocks/682C31EA2C31B3C2/project/Data/RoadSegmentBehaviourAnalysis/DataSet/ByAbhijit/Bus/Date_20_09_17ukhra/DATA_17_12_44/Light/Bus_Rating.txt'
for i in range(0,6):
	if not os.path.exists(busy_folder+str(i)):
		os.makedirs(busy_folder+str(i))
rate_data={}
rating_data=np.loadtxt(rating_file,dtype=datatype,delimiter=',')
#print rating_data
for i in range(len(rating_data)):
	temp=rating_data['time'][i].split(' ')[2]
	temp=temp.split(':')
	temp=int(temp[0])*3600+int(temp[1])*60+int(temp[2])
	rating_data['time'][i]=int(temp)
	#rate_data[temp]=data['rate']
#for data in rating_data:
#		print data

print(len(rating_data))

list_files=check_output('ls '+busy_folder,shell=True).split('\n')
for files in list_files:
	#print "working on", files
	if not os.path.isdir(busy_folder+files):
		open_file=open(busy_folder+files,'r')
		data=open_file.read().split('\n')
		#open_file=np.loadtxt(busy_folder+files,dtype=busy_datatype,delimiter=',')
		n=len(data)-1
		time_=data[n-1].split(',')[2]
		time_=time_.split(':')
		time_=int(time_[0])*3600+int(time_[1])*60+int(time_[2])
		open_file.close()
		for data in rating_data:
			if int(data['time'])>=time_:
				print(data['time'],time)
				command = 'mv '+busy_folder+files+' '+busy_folder+str(data['rate'])+'/'
				#print command
				os.system(command)
				break
for i in range(0,6):
	tag_folder = busy_folder + str(i) + '/'
	os.system('cat '+tag_folder+'Busy* > '+busy_folder+str(i)+'.csv')