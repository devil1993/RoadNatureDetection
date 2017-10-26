import sys
from extractData import get_spherical_distance
file_name = sys.argv[1]

f = open(file_name,'r')
lines = f.read().split('\n')
f.close()

out_file = sys.argv[2]
f= open(out_file,'w')

pointSet = []
#Extract the point and timestamp from the lines
for line in lines:
        components = line.split(',')
        try:
                point_x = float(components[0])
                point_y = float(components[1])
                #split time into hours, minutes and seconds
                timeunits = components[4].split(' ')[1].split(':')
                #convert the time into seconds
                point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
                
                pointSet += [(point_x,point_y,point_t)]
        except Exception, e:
			print e

print(pointSet)
length = float(sys.argv[3])

dist = 0

for i in range(1,len(pointSet)):
	d = get_spherical_distance(pointSet[i][0],pointSet[i-1][0],pointSet[i][1],pointSet[i-1][1])
	print(dist)
	dist += d
	if(dist>length):
		dist = 0
		f.write(str(pointSet[i][0])+','+str(pointSet[i][1])+'\n')
f.close()