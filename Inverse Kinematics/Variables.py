# Time delay sets delay in each loop in millis
time_delay = 30

# Sets screen width and height in pixels
screen_dimension = 800

# Screen width and height in inches for math
screen_dimension_inches = 24

# Screen multiplier
multiplier = 2

# Link Lengths in inches (Thigh, crank, coupler, follower, calf, hip)
linkLength1 = 4.5
linkLength2 = 1.5
linkLength3 = 4.5
linkLength4 = 1.5
linkLength5 = 6.5 - linkLength4
linkLengthhip = 2

linkLength1 *= multiplier
linkLength2 *= multiplier
linkLength3 *= multiplier
linkLength4 *= multiplier
linkLength5 *= multiplier
linkLengthhip *= multiplier

# Mechanism origin in screen (for visuals only)
origin_x = screen_dimension_inches / 2
origin_y = screen_dimension_inches / 4

# Colors
red = (255, 10, 92)
orange = (255, 95, 10)
yellow = (255, 180, 0)
green = (25, 100, 25)
blue = (0, 200, 250)
purple = (100, 10, 100)
gray = (50, 50, 50)
white = (255, 255, 255)
black = (10, 10, 10)