
# goal is to track the car's position through motor movement.

# records the direction 
relative_theta = 0

# position in cm
starting_pos = []
prev_pos = []
curr_pos = [0,0] 

# speed is the same wether it turns left or right
turn_meter = Odometer(12, 22)


# turns car a specific distance
def turn_right(power, angle):
    
    dist = angle_to_dist(angle)
    turn_meter.reset()
    turn_meter.start()
    fc.forward(power)
    while(turn_meter.distance < dist):
        continue
    
    fc.stop()



def new_pos():
    continue

# calculates the relative distance moved
def distance_moved(prev_dist):
    #ultrasonic reading2 - ultrasonic reading1   
    curr_dist = fc.get_distance_at(0)
    
    return curr_dist - prev_dist



def angle_to_dist(angle, radius = 7):
    
    rot = angle / 360
    circumference = 2 * radius * math.pi

    return rot * circumference
    

def rotation(curr_theta, start_dist, end_dist):

    # distance between front wheels ia about 14cm    
    d = 14 
    r = 7
    circumference = d * math.pi 
    
    radians  = (end_dist - start_dist) / r


    # convert to degrees
    deg = radians * (180 / pi)

    return  int(curr_theta + deg) % 360

