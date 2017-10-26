import sys
import os

# print 'Starting NEMO------------------------------------------------------'

folder = './'
try:
	folder = sys.argv[5]
except Exception,e:
	print e

gps_file_name  = folder + sys.argv[1]
sound_file_name  = folder + sys.argv[2]
wifi_file_name  = folder + sys.argv[3]

file = open(gps_file_name,'r')
gps_strings = file.read().split('\n')
file.close()

file = open(sound_file_name,'r')
sound_strings = file.read().split('\n')
file.close()


file = open(wifi_file_name,'r')
wifi_strings = file.read().split('\n')
file.close()


gps = []
sounds = []
wifis = []

for gps_string in gps_strings:
	try:
		components = gps_string.split(',')
		gps = gps + [(components[0], components[1],components[4].split(' ')[1],components[5])]
	except Exception,e:
		print e
for sound_string in sound_strings:
	try:
		components = sound_string.split(',')
		sounds = sounds + [(components[0], components[1],components[2])]
	except Exception,e:
		print e

for wifi_string in wifi_strings:
	try:
		components = wifi_string.split(',')
		wifis = wifis + [(components[0], components[1], components[2], components[3])]
	except Exception,e:
		print e

#sizes = max([len(gps),len(gps),len(gps)])

#print sounds

# print wifis

j=0
k=0
res = []

for i in xrange(0,len(gps)):
	lat = gps[i][0]
	lng = gps[i][1]
	time = gps[i][2]
	info = gps[i][3]
	# print lat,lng,time
	sound_data = -1
	sound_dev = 0
	#print sounds[j][0],time
	while (j<len(sounds) and sounds[j][0]<=time):
		#  print sounds[j][0]
		# print sounds[j][0],time
		if(sounds[j][0]==time):
			sound_data = sounds[j][1]
			sound_dev = sounds[j][2]
		j = j+1
	
	wifi_data = []
	while (k<len(wifis) and wifis[k][3][11:]<=time):
		# print wifis[k][3][11:],time
		if (wifis[k][3][11:] == time):
			wifi_data = wifi_data + [(wifis[k][0],wifis[k][1],int(wifis[k][2]))]
			# print wifi_data
		k = k+1
		
	
	#print wifi_data
	#res = res + [(lat,lng,time,sound_data,wifi_data)]
	res = res + [(lat,lng,time,sound_data,sound_dev,wifi_data,info)]
if not os.path.exists(folder+'tags'):
    os.makedirs(folder+'tags')
file = open(folder + sys.argv[4],'w')
try:
	for result in res:		
		file.write(result[0]+','+result[1]+','+result[2]+','+str(result[3])+','+str(result[4])+','+str(result[5])+'\n')
		#print result[6]
		tags = result[6].split('+')
		if len(tags)>1:
			for tag in tags:
				if tag == '':
					continue
				try:
					tag_folder = tag.split('_')[0].replace(' ','_')					
					if not os.path.exists(folder+'tags/'+tag_folder):
						os.makedirs(folder+'tags/'+tag_folder)
					tag_name = tag.replace(' ','_')
					# print folder+tag_name+sys.argv[1]
					splitFile = open(folder+'tags/'+tag_folder+'/'+tag_name+sys.argv[1],'a')
					splitFile.write(result[0]+','+result[1]+','+result[2]+','+str(result[3])+','+str(result[4])+','+str(result[5])+'\n')
					splitFile.close()
				except Exception,e:
					print e
		#file.write(result[0]+','+result[1]+','+result[2]+','+'\n')
except Exception,e:
	print e
file.close()