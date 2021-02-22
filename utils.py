

# various utiliy functions that may be useful for calcuations



def angle_to_dist(angle, radius = 7):
    
    rot = angle / 360
    circumference = 2 * radius * math.pi

    return rot * circumference
    
def dist_to_angle(dist, radius = 7):
    circumference = 2 * radius * math.pi

    # only last rotation matters
    rot = (dist // circumference) - (dist / circumference)

    return rot * 360
    


# checks how far the car has rotated
def rotation(curr_theta, start_dist, end_dist):

    # distance between front wheels ia about 14cm    
    d = 14 
    r = 7
    circumference = d * math.pi 
    
    radians  = (end_dist - start_dist) / r


    # convert to degrees
    deg = radians * (180 / math.pi)

    return  int(curr_theta + deg) % 360
