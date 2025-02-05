import DistancetoGoal as Dist
import Thrust
from time import sleep
import GPStest as gps
import mag
TargetRadius = 10                       #Target radius in meters for the moving to end.
#state = 0                               #state = 0: All thrusters off
#state = 1                              #state = 1: Rear thrusters thrusting forward
#state = 2                              #state = 2: Rear thrusters thrusting forward and front thruster turning GAUSS right
#state = 3                              #state = 3: Rear thrusters thrusting forward and front thruster turning GAUSS left
#state = 4                              #state = 4: Rear thrusters off and front thruster is turning GAUSS right
#state = 5                              #state = 5: Rear thrusters off and front thruster is turning GAUSS left
#state = 6
forward_thrust = 1950
reverse_thrust = 1850
turn_right = 1950
turn_left = 1850
inc = 60
gain = 2

def Move(targetLat, targetLong):
    gps.GPSinit()
    gaussLat = 0
    gaussLong = 0
    headMax = 0
    while Dist.getGoalDistance(gaussLat, gaussLong, targetLat, targetLong) > TargetRadius:
       gaussCoords = gps.GPSrun(10)
       print("got the coordinates")
       gaussLat = gaussCoords[0]
       gaussLong = gaussCoords[1]
       print(gaussLat)
       print(gaussLong)
       print("target long", targetLong)
       print("target lat", targetLat)
       gaussHead = mag.get_head()
       goalHead = Dist.getGoalHeading(gaussLat, gaussLong, targetLat, targetLong)

       headDiff = gaussHead - goalHead
       HeadingError = abs(headDiff)
       if HeadingError > 180:
           HeadingError -= 360
       elif HeadingError < -180:
           HeadingError += 360
       print("Distance to goal: ", Dist.getGoalDistance(gaussLat, gaussLong, targetLat, targetLong)," Meters")
       print("Goal Heading: ",goalHead," deg")
       print("Gauss Heading: ",gaussHead,"deg")
       print("Heading Error: ",HeadingError,"deg")
       sleep(.5)
       if HeadingError > 30:
            headMax = 30
       else:
            headMax = HeadingError
       if HeadingError < 10:
            state = 1
       elif HeadingError < 30:
            if headDiff < 0:
                state = 2
            else:
                state = 3
       else:
            if headDiff < 0:
                state = 4
            else:
                state = 5
       if state == 0:
           Thrust.stop(3)
       elif state == 1:
           Thrust.ramp(3, forward_thrust)
       elif state == 2:
           Thrust.ramp(3, forward_thrust)
           Thrust.ramp(0, turn_right + headMax*gain)
       elif state == 3:
           Thrust.ramp(3, forward_thrust)
           Thrust.ramp(0, turn_left - headMax*gain)
       elif state == 4:
           Thrust.stop(2)
           Thrust.stop(1)
           Thrust.ramp(0, turn_right + inc)
       else:
           Thrust.stop(2)
           Thrust.stop(1)
           Thrust.ramp(0, turn_left - inc)
       sleep(.5)
    Thrust.stop(3)
    print("I have reached the goal sire")

