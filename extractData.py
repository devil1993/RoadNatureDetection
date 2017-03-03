import sys
import os
from math import *
import math
import numpy as np
import ast
from settings import *

stop_radius = 0 
input_file = ' '
output_file = ' '
ground_truth_file =  ' '
pointSet = []
input_dir = './'
def get_spherical_distance(lat1,lat2,long1,long2):
        """
        Get spherical distance any two points given their co-ordinates (latitude, longitude)
        """
        q=radians(lat2-lat1)
        r=radians(long2-long1)
        lat2r=radians(lat2)
        lat1r=radians(lat1)
        a=sin(q/2)*sin(q/2)+cos(lat1r)*cos(lat2r)*sin(r/2)*sin(r/2)
        c=2*atan2(sqrt(a),sqrt(1-a))
        R=6371*1000
        d=R*c
        return d

def computeStats(stop,start,stop_no,stop_distances_list):
	#Mark the pointSet list as global to use the global pointSet
	global pointSet
	#Calculate the time difference
	time_diff = stop - start
	#print "time diff:",time_diff
	#We can calculate the mean speed from the total distance and time taken to reach the current stop
	mean = stop_distances_list[stop_no]/time_diff
	#initialize varience as zero and then add up the squred distances later
	varience = 0.0
	#Now we check all the points in the concerned range
	for x in range(start-1,stop-1):
		try:
			_lastPoint = pointSet[x]
			_point = pointSet[x+1]
			#We check the distance between two consecutive points as the speed in m/s unit
			dspeed = get_spherical_distance(_point[0],_lastPoint[0],_point[1],_lastPoint[1])
			#Add up to the varience
			varience = varience + math.pow(mean - dspeed ,2)
		except Exception,e:
			print e
	#Actual varience is [Sum of squred differences/The number of samples] and the Standard Deviation is the root of the varience
	sd = math.sqrt(varience/time_diff)
	return (mean,sd)	

def initialize_single():
	'''
	This function initializes the configurations for getting info from single input file
	'''
	global stop_radius,ground_truth_file,input_file,output_file

	stop_radius = int(config["stop_length"])/2
	ground_truth_file = config["ground_truth_file"]
	output_file = config["output_file_prefix"]

	input_file = sys.argv[1]

	try:
		output_file = sys.argv[2]
	except Exception, e:
		print "Taking output file name from config file..."

def initialize_multi(source_directory):
	'''
	This function initializes the configurations for getting info from single input file
	'''
	global stop_radius,ground_truth_file,input_file,output_file,input_dir
	with open('config.txt','r') as inf:
	    config = eval(inf.read())

	stop_radius = int(config["stop_length"])/2
	ground_truth_file = config["ground_truth_file"]
	output_file = source_directory + '/results/' + config["output_file_prefix"]
	input_dir = source_directory+'/'
	#input_file = sys.argv[1]

	try:
		output_file = sys.argv[2]
	except Exception, e:
		print "Taking output file name from config file..."

def getInfo(input_file):
	global pointSet
	#Read the whole input file
	file = open(input_dir+input_file,"r")
	lines = file.read().split('\n')
	file.close()

	pointSet = []
	#Extract the point and timestamp from the lines
	for line in lines:
	        components = line.split(',')
	        try:
	                point_x = float(components[0])
	                point_y = float(components[1])
	                #split time into hours, minutes and seconds
	                timeunits = components[2].split(':')
	                #convert the time into seconds
	                point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
	                #pointSet.insert(len(pointSet), (point_x,point_y,point_t))
	                point_sm = float(components[3])
	                point_ssd = float(components[4])
	                list_start = line.index('[')
	                wifis = ast.literal_eval(line[list_start:])
	                pointSet += [(point_x,point_y,point_t,point_sm,point_ssd,wifis)]
	        except Exception, e:
				print e

	#Read the ground truth file			
	file = open(ground_truth_file,"r")
	lines = file.read().split('\n')
	file.close()

	groundTruthPointSet = []
	#Create the set of ground truth points from file
	for line in lines:
	        components = line.split(',')
	        try:
	                point_x = float(components[0])
	                point_y = float(components[1])
	                #timeunits = components[2].split(':')
	                #point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
	                #pointSet.insert(len(pointSet), (point_x,point_y,point_t))
	                groundTruthPointSet += [(point_x,point_y)]
	        except Exception, e:
	                #print e
	                pass
	#print groundTruthPointSet, len(groundTruthPointSet)
	totalStops = len(groundTruthPointSet)
	currentStop = 0 # denotes the current stop number
	#Initialize the results
	routeLength = 0.0
	stop_distances = [0.0]*(totalStops)
	path_details = [(0.0,0.0)]*(totalStops)
	stop_times = [0] * totalStops
	wait_times = [0] * totalStops
	reaching_time = [0] * totalStops
	wifi_list = []
	wifi_found = []
	wifi_index = []
	lastPoint = pointSet[0]
	# j and i indicates the starting and ending points of a path between stops respectively
	i = 0
	j = 0

	starting_time = pointSet[0][2]
	nearest_stop = 0
	nearest_stop_distance = 0
	distances_from_stops = 9999
	for i in range(0,len(groundTruthPointSet)):
		d = get_spherical_distance(lastPoint[0],groundTruthPointSet[i][0],lastPoint[1],groundTruthPointSet[i][1])
		print d
		if d<distances_from_stops:
			distances_from_stops = d
			nearest_stop = i
	currentStop = nearest_stop
	# Check if the vehicle is at an moving state with respect to the first stop
	movingFlag = get_spherical_distance(lastPoint[0],groundTruthPointSet[currentStop][0],lastPoint[1],groundTruthPointSet[currentStop][1]) > stop_radius
	speed_sign = []
	# Now we traverse through the points set
	for point in pointSet:
		# Recheck current stop for the first time
		if currentStop == nearest_stop:
			new_nearest_stop = currentStop
			for i in range(0,len(groundTruthPointSet)):
				d = get_spherical_distance(lastPoint[0],groundTruthPointSet[i][0],lastPoint[1],groundTruthPointSet[i][1])
				print d
				if d<distances_from_stops:
					distances_from_stops = d
					new_nearest_stop = i
			currentStop = new_nearest_stop
		# If the trail catches the points beyond the last stop, we ignore it.
		if(currentStop == totalStops):
			#print 'oops'
			continue
		# d is the distance from the last point in the trail
		d = get_spherical_distance(point[0],lastPoint[0],point[1],lastPoint[1])
		#print d,currentStop,i
		# If we are in the range of the next stop
		if get_spherical_distance(point[0],groundTruthPointSet[currentStop][0],point[1],groundTruthPointSet[currentStop][1]) < stop_radius:
			# If we were moving earlier and came to a stop, compute the stats from starting and ending point of the trail and the distance covered.
			#print 'stopped in stopage'
			if movingFlag:
				if currentStop ==0:
					starting_time = pointSet[i][2]
				reaching_time[currentStop] = point[2]
				#print 'came to ',currentStop, groundTruthPointSet[currentStop],len(speed_sign)
				if not os.path.exists(input_dir+'results/subRoute'+str(currentStop)):
    					os.makedirs(input_dir+'results/subRoute'+str(currentStop))
				filedetails = open(input_dir+'results/subRoute'+str(currentStop)+'/'+input_file,'w')
				
				mean_sound = 0
				sd_sound = 0

				try:
					sign = np.array(speed_sign)
					mean_sound = np.mean(sign[:,2])
					sd_sound = np.std(sign[:,2])
				except Exception as e:
					print e
				
				#'''
				for x in speed_sign:
					normal_sound = (x[2]-mean_sound)/sd_sound
					# distance instant_speed instant_max_sound instant_sd_sound instant_normalized_max_sound				
					filedetails.write(str(x[1])+'\t'+str(x[0])+'\t'+str(x[2])+'\t'+str(x[3])+'\t'+str(normal_sound)+'\n')
				filedetails.close()
				speed_sign = []
				path_details[currentStop] = computeStats(i,j,currentStop,stop_distances)
			# Set the flag as false as it has entered a stop area
			movingFlag = False
			# Increase the wait point of the current stop by the time difference which is 1
			wait_times[currentStop] = wait_times[currentStop] + 1
			# if the vehicle has not moved since its last position, we add one second to the stop time.
			if d == 0:
				stop_times[currentStop] = stop_times[currentStop] + 1
		else:
			# We are not in the range of a stop - thus we are in a moving mode
			# Increase the route length by the distance traveled
			routeLength = routeLength + d
			# If the vehicle is in moving state we add the distance travelled to the distance between stops.
			if movingFlag:
				stop_distances[currentStop] = stop_distances[currentStop] + d
				speed_sign = speed_sign + [(d,stop_distances[currentStop],point[3],point[4])]
				for wifi in point[5]:
					if wifi[1] not in wifi_found:
						wifi_found.append(wifi[1])
			else:
				# Else it has moved to a moving state from a static state, so we can now compute for the next stop
				#print i
				if not(i==0):
					#print 'here', currentStop,'to', currentStop+1,i
					currentStop = currentStop + 1
					wifi_index = wifi_index + [currentStop-1]
					wifi_list = wifi_list + [wifi_found[:]]
					wifi_found = []
				# Coputing for the next stop/path to the next stop, so we set a new starting point here
				j = i
			#Now the vehicle is moving, thus we change the state
			movingFlag = True
		# set current point as last point for next iteration and chage the counter
		lastPoint = point
		i = i+1
	#print i, len(pointSet), movingFlag
	# Write data to output file
	file = open(output_file + input_file + '_' + str(starting_time),"w")
	#file.write('location lat, location long,stop time,wait time,distance from last stop, mean speed in m/s, standard deviation of speed'+'\n')
	for x in xrange(0,totalStops):		
		line = str(groundTruthPointSet[x][0]);
		line = line + ',' + str(groundTruthPointSet[x][1])
		#line = line + ',' + '\'' + str(reaching_time[x]/3600) + ':' + str((reaching_time[x]%3600)/60) + ':' + str((reaching_time[x]%3600)%60)+ '\'' 
		line = line + ',' + str(reaching_time[x])
		line = line + ',' + str(stop_times[x])
		line = line + ',' + str(wait_times[x])
		line = line + ',' + str(stop_distances[x])
		line = line + ',' + str(path_details[x][0])
		line = line + ',' + str(path_details[x][1])
		line = line + ',' + str(x)
		if x in wifi_index and stop_distances[x]>0:
			line = line + ',' + str(len(wifi_list[wifi_index.index(x)])/stop_distances[x])
		else:
			line = line + ',0'
		line = line + '\n'
		file.write(line)
	file.close()


# Calls to functions to execte the file through command line
'''
initialize_single()
getInfo(input_file)
'''
# Bye :)
