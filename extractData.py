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
	speedset = []
	for x in range(start-1,stop-1):
		try:
			_lastPoint = pointSet[x]
			_point = pointSet[x+1]
			#We check the distance between two consecutive points as the speed in m/s unit
			dspeed = get_spherical_distance(_point[0],_lastPoint[0],_point[1],_lastPoint[1])
			#Add up to the varience
			speedset = speedset + [dspeed]
			varience = varience + math.pow(mean - dspeed ,2)
		except Exception as e:
			print(e)
	#Actual varience is [Sum of squred differences/The number of samples] and the Standard Deviation is the root of the varience
	sd = math.sqrt(varience/time_diff)
	npspeedset = np.array(speedset)
	mean = np.mean(npspeedset)
	sd = np.std(npspeedset)
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
	except Exception as e:
		print("Taking output file name from config file...")

def initialize_multi(source_directory,stopfile = config["ground_truth_file"]
	,out_dir = None):
	'''
	This function initializes the configurations for getting info from single input file
	'''
	global stop_radius,ground_truth_file,input_file,output_file,input_dir
	if out_dir == None:
		output_file = source_directory + '/results/'
	else:
		output_file = out_dir
	#with open('config.txt','r') as inf:
	#    config = eval(inf.read())

	stop_radius = int(config["stop_length"])/2
	ground_truth_file = stopfile
	
	input_dir = source_directory
	#input_file = sys.argv[1]

	# try:
	# 	output_file = sys.argv[2]
	# except Exception as e:
	# 	print("Taking output file name from config file...")
def find_nearest_stop(x,y,j,groundTruthPointSet):
	#global  groundTruthPointSet
	new_nearest_stop = 0
	nearest_stop_distance = 0
	distances_from_stops = 9999
	end=len(groundTruthPointSet)
	for i in range(j,end):
		d = get_spherical_distance(x,groundTruthPointSet[i][0],y,groundTruthPointSet[i][1])
		# print i,d
		if d<distances_from_stops:
			distances_from_stops = d
			new_nearest_stop = i
	return new_nearest_stop
def getInfo(input_file):
	global pointSet
	#Read the whole input file
	file = open(input_dir+input_file,"r")
	lines = file.read().split('\n')
	file.close()

	
	# ip_file_identifiers = input_file.split('_')
	# file_identifier = ip_file_identifiers[-7]+ip_file_identifiers[-6]+ip_file_identifiers[-5]
	
	file_identifier = input_file.split('.')[0]

	# print file_identifier
	# sys.exit(1)

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
				point_rating = float(components[3])
				point_speed = float(components[4])
				point_alt = float(components[5])
				list_start = line.index('[')
				wifis = ast.literal_eval(line[list_start:])
				pointSet += [(point_x,point_y,point_t,point_rating,point_speed,wifis,point_alt)]
			except Exception as e:
				print(e)

	#Read the ground truth file	
	print(ground_truth_file)		
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
	        except Exception as e:
	                #print e
	                pass
	#print groundTruthPointSet, len(groundTruthPointSet)
	totalStops = len(groundTruthPointSet)
	currentStop = 0 # denotes the current stop number
	#Initialize the results
	routeLength = 0.0
	stop_distances = [0.0]*(totalStops)
	path_details = [(0.0,0.0)]*(totalStops)
	alt_devs = [0.0]*(totalStops)
	stop_times = [0] * totalStops
	wait_times = [0] * totalStops
	reaching_time = [0] * totalStops
	slow_speed_fraction = [-1.0] * totalStops
	# sound_feature =[0.0]*totalStops
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
	#Finding the bus stop trail to first bus stop. 
	'''for i in range(0,len(groundTruthPointSet)):
		d = get_spherical_distance(lastPoint[0],groundTruthPointSet[i][0],lastPoint[1],groundTruthPointSet[i][1]) # call the function to get the distance between point given as argument
		# print d
		if d<distances_from_stops:
			distances_from_stops = d
			nearest_stop = i 	# tracks the nearest stop to first GPS trail 
	'''
	#currentStop = nearest_stop
	nearest_stop=find_nearest_stop(lastPoint[0],lastPoint[1],0,groundTruthPointSet)
	currentStop = nearest_stop
	print("Current Stop:-",currentStop)
	# Check if the vehicle is at an moving state with respect to the first stop
	movingFlag = get_spherical_distance(lastPoint[0],groundTruthPointSet[currentStop][0],lastPoint[1],groundTruthPointSet[currentStop][1]) > stop_radius
	speed_sign = []
	alts = []
	last_time = starting_time
	# Now we traverse through the points set
	for point in pointSet:
		# Recheck current stop for the first time
		# print currentStop
		#	_time = point[2]
		#	timetaken = _time - last_time
		if(point[2]-lastPoint[2]>5):
			nearest_stop=find_nearest_stop(point[0],point[1],currentStop,groundTruthPointSet)
			currentStop=nearest_stop
			lastPoint=point
			# currentStop+=1
			print(currentStop,lastPoint)
			# continue
		elif(point[2]-lastPoint[2]<1):
			continue
		if currentStop == nearest_stop:
			currentStop = find_nearest_stop(point[0],point[1],0,groundTruthPointSet)
			'''for i in range(0,len(groundTruthPointSet)):
				d = get_spherical_distance(lastPoint[0],groundTruthPointSet[i][0],lastPoint[1],groundTruthPointSet[i][1])
				# print i,d
				if d<distances_from_stops:
					distances_from_stops = d
					new_nearest_stop = i
			currentStop = new_nearest_stop'''
			# currentStop=new_nearest_stop
		# If the trail catches the points beyond the last stop, we ignore it.
		if(currentStop == totalStops):
			continue
		# print "Current Stop:",currentStop
		# d is the distance from the last point in the trail
		d = get_spherical_distance(point[0],lastPoint[0],point[1],lastPoint[1])
		#print d,currentStop,i
		# If we are in the range of the next stop
		distFrmStp = get_spherical_distance(point[0],groundTruthPointSet[currentStop][0],point[1],groundTruthPointSet[currentStop][1])
		#print 'distFrmStp',currentStop, distFrmStp,d
		if  distFrmStp < stop_radius:
			# If we were moving earlier and came to a stop, compute the stats from starting and ending point of the trail and the distance covered.
			#print 'stopped in stopage'
			if movingFlag:
				routeLength = routeLength + d
				if currentStop ==0:
					starting_time = pointSet[i][2]
				reaching_time[currentStop] = point[2]
				#print 'came to ',currentStop, groundTruthPointSet[currentStop],len(speed_sign)
				if not os.path.exists(output_file + 'subRoute'+str(currentStop)):
    					os.makedirs(output_file + 'subRoute'+str(currentStop))
				filedetails = open(output_file + 'subRoute'+str(currentStop)+'/'+input_file,'w')
				
				mean_sound = 0
				sd_sound = 0
				mean_speed = 0
				sd_speed = 0

				# try:
				# 	sign = np.array(speed_sign)
				# 	mean_sound = np.mean(sign[:,2])
				# 	sd_sound = np.std(sign[:,2])
				# 	mean_speed = np.mean(sign[:,0])
				# 	sd_speed = np.std(sign[:,0])
				# except Exception as e:
				# 	print(e)
				
				#'''
				cum_distance = 0.0
				sound_data = 0.0
				for x in speed_sign:
					# normal_sound = (x[2]-mean_sound)/sd_sound
					# if x[2] > sound_threshold:
					# 	sound_data = sound_data +(x[2] - sound_threshold)*(x[0]+1)
					# if x[2] > 0:
					# 	cum_distance = cum_distance + x[0]
					# distance instant_speed instant_max_sound instant_sd_sound instant_normalized_max_sound				
					filedetails.write(str(x[1])+'\t'+str(x[0])+'\t'+str(x[2])+'\t'+str(x[3])+'\n')
				filedetails.close()
				try:
					slow_points = [x for x in speed_sign if x[0]<threshold_speed]
					slow_speed_fraction[currentStop] = float(len(slow_points))/len(speed_sign)					
				except Exception as e:
					print(e)
				# try:
				# 	sound_feature[currentStop] = sound_data/cum_distance
				# except Exception as e:
				# 	print(e)
				cur_alt_dev = np.std(alts)
				speed_sign = []
				alts = []
				alt_devs[currentStop] = cur_alt_dev
				#path_details[currentStop] = computeStats(i,j,currentStop,stop_distances)
				path_details[currentStop] = (mean_speed,sd_speed)
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
				alts = alts + [point[6]]
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
	file = open(output_file + input_file + '_' + str(starting_time)+'.csv',"w")
	file.write('#location_lat,location_long,reaching_time,stop_time,wait_time,distance_from_last_stop,mean_speed_in_m/s,standard_deviation of speed,stop number,slow speed fraction,sound feature,wifi density'.replace(' ','_')+ ',alt_devs' + '\n')
	for x in range(0,totalStops):
		if(path_details[x][0]<=0):
			continue
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
		line = line + ',' + str(slow_speed_fraction[x])
		# line = line + ',' + str(sound_feature[x])
		if x in wifi_index and stop_distances[x]>0:
			line = line + ',' + str(len(wifi_list[wifi_index.index(x)])/stop_distances[x])
		else:
			line = line + ',0'
		line = line + ',' + file_identifier 
		line = line + ',' + str(alt_devs[x]) + '\n'
		# line = line + '\n'
		file.write(line)
	file.close()


# Calls to functions to execte the file through command line
'''
initialize_single()
getInfo(input_file)
'''
# Bye :)