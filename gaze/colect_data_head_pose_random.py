import time
import csv
from playsound import playsound
import sys
import random
import zmq

def main(filename, player):    
    port = "5000"

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting head pose updates...")

    socket.connect ("tcp://localhost:%s" % port)
    topic_filter = b'HeadPose:'
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

    poses = {"free_Shrek": 0, "free_Robot": 0, "free_Center": 0, "free_Tablet":0, "glance_Shrek": 0, "glance_Robot": 0, "glance_Center": 0, "glance_Tablet":0 }
    data = {"Shrek":[], "Robot":[], "Center":[], "Tablet":[]}



    previous = "glance_"
    for iteration in range(32):
                pos = [label for label, value in poses.items() if value < 4 and previous not in label]
                if pos == [] :
                       pos = [label for label, value in poses.items() if value < 4]
                pose = random.choice(pos)
                poses[pose] += 1
                if "free_" in pose:
                      previous = pose[5:]
                if "glance_" in pose:
                      previous = pose[7:]
                print(pose)
                f = pose+".mp3"
                playsound(f)
                print(poses)

                i = 0
                data_pose = []
                while i < 100:
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
                    data_pose.append([X, Y, Z, pitch, yaw, roll])
                    i+=1
                    time.sleep(0.01)
                
                if "free_" in pose:
                      pose = pose[5:]
                if "glance_" in pose:
                      pose = pose[7:]
                print(pose)
                data[pose] += data_pose
    
    playsound("bip.mp3")
    filename = "data\\" + player + "\\"+ filename + ".tsv"
    with open(filename, 'w', encoding='utf8', newline='') as tsv_file:
                tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
                for pose in data.keys():
                      tsv_writer.writerow([pose])
                      for line in data[pose]:
                            tsv_writer.writerow(line)
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])