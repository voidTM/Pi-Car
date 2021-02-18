
# goal is to track the car's position through motor movement.

# records the direction 
relative_theta = 0

# position in cm
starting_pos = []
prev_pos = []
curr_pos = [0,0] 

# speed is the same wether it turns left or right

def turn_right(angle):
    continue


def new_pos():
    continue

# calculates the relative distance moved
def distance_moved(prev_dist):
    #ultrasonic reading2 - ultrasonic reading1   
    curr_dist = fc.get_distance_at(0)
    
    return curr_dist - prev_dist



def rotation(curr_theta, start_dist, end_dist):

    # distance between front wheels ia about 14cm    
    d = 14 
    r = 7
    circumference = d * math.pi 
    
    radians  = (end_dist - start_dist) / r


    # convert to degrees
    deg = radians * (180 / pi)

    return  int(curr_theta + deg) % 360

