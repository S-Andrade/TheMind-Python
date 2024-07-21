import time
import xlsxwriter

def main():

    import zmq
    port = "5000"

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting head pose updates...")

    socket.connect ("tcp://localhost:%s" % port)
    topic_filter = b'HeadPose:'
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

    while True:
        head_pose = socket.recv()
        head_pose = head_pose.decode()
        head_pose = head_pose[9:].split(', ')
        head_pose = [hp.replace(',', '.') for hp in head_pose]
        X = float(head_pose[0])
        Y = float(head_pose[1])
        Z = float(head_pose[2])

        pitch = float(head_pose[3])
        yaw = float(head_pose[4])
        roll = float(head_pose[5])



        if  X >= 57.76 and X <= 121.76 and Y >= 24.59 and Y <= 42.77 and Z >= 479.79 and Z <= 525.37 and pitch >= -6.13 and pitch <= 10.53 and yaw >= -31.95 and yaw <= 10.79 and roll >= -0.86 and roll <= 12.61: 
            print("Left")

        if  X >= -61.85 and X <= 101.55 and Y >= 11.99 and Y <= 34.72 and Z >= 440.83 and Z <= 498.8 and pitch >= -9.55 and pitch <= 6.25 and yaw >= -30.92 and yaw <= 39.95 and roll >= -6.85 and roll <= 12.48: 
            print("Right")
        
        if  X >= -63.69 and X <= 58.99 and Y >= 15.24 and Y <= 57.55 and Z >= 448.64 and Z <= 484.64 and pitch >= -9.71 and pitch <= 7.6 and yaw >= 0.1 and yaw <= 39.52 and roll >= -1.72 and roll <= 5.31: 
            print("Down")

        if  X >= 49.53 and X <= 65.64 and Y >= 35.37 and Y <= 53.52 and Z >= 445.37 and Z <= 471.43 and pitch >= -1.38 and pitch <= 8.69 and yaw >= 0.97 and yaw <= 7.87 and roll >= -3.88 and roll <= -1.16: 
            print("Front")

        #time.sleep(0.01)



if __name__ == '__main__':
    main()