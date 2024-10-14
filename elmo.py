from ElmoV2API import ElmoV2API
import time

robot_ip = "192.168.0.102"
robot = ElmoV2API(robot_ip, debug=False)
robot.enable_behavior(name="look_around", control = False)
robot.enable_behavior(name="blush", control = False)
# look neutral
robot.set_pan(0)
robot.set_tilt(-5)
robot.set_pan_torque(True)
robot.set_tilt_torque(True)
robot.set_screen(image="simple-think.gif")
robot.update_leds_icon("nothing.png")

time.sleep(5)

"""# look at player0 
robot.set_pan(-20)
robot.set_tilt(-5)
time.sleep(5)

# look at player1
robot.set_pan(20)
robot.set_tilt(-5)
time.sleep(5)

# look neutral
robot.set_pan(0)
robot.set_tilt(-5)
time.sleep(5)

#look at tablet
robot.set_pan(0)
robot.set_tilt(15)
time.sleep(5)"""

#look at mainscreen
robot.set_pan(0)
robot.set_tilt(0)

#TODO  FAZ ROBO
