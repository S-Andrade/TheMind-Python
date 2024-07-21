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
        print(head_pose)
        head_pose = head_pose[9:].split(', ')
        print(head_pose)
        """X = float(head_pose[0])
        Y = float(head_pose[1])
        Z = float(head_pose[2])

        pitch = float(head_pose[3])
        yaw = float(head_pose[4])
        roll = float(head_pose[5])"""




        time.sleep(0.01)



if __name__ == '__main__':
    main()