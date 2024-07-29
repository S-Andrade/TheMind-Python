from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from xlrd import open_workbook
import csv
import numpy as np
import zmq
import time
import pygame
import glob, os
import joblib


def getData():
    pose = ""
    X = []
    y = []

    os.chdir("data\\player0")
    for file in glob.glob("*.tsv"):    
        with open(file, encoding="utf-8") as file:       
            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                if len(line) == 1:
                    pose = line[0]
                else:
                    X.append(line)
                    y.append(pose)
    return np.array(X), np.array(y)

def training(X,y):
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80, test_size=0.20, random_state=101)
    rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
    poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X_train, y_train)

    poly_pred = poly.predict(X_test)
    rbf_pred = rbf.predict(X_test)

    poly_accuracy = accuracy_score(y_test, poly_pred)
    poly_f1 = f1_score(y_test, poly_pred, average='weighted')
    print('Accuracy (Polynomial Kernel): ', "%.2f" % (poly_accuracy*100))
    print('F1 (Polynomial Kernel): ', "%.2f" % (poly_f1*100))

    rbf_accuracy = accuracy_score(y_test, rbf_pred)
    rbf_f1 = f1_score(y_test, rbf_pred, average='weighted')
    print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
    print('F1 (RBF Kernel): ', "%.2f" % (rbf_f1*100))

    return poly, rbf

def trainingAll(X,y):
    
    rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X, y)
    poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X, y)

    return poly, rbf

def run(poly, rbf):
    port = "5000"

    pygame.init()
 
    screen = pygame.display.set_mode((550, 200))
    
    
    pygame.display.set_caption('SVM')

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting head pose updates...")

    socket.connect ("tcp://localhost:%s" % port)
    topic_filter = b'HeadPose:'
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

    while True:
        pygame.event.get()
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

        poly_pred = poly.predict([[X, Y, Z, pitch, yaw, roll]])
        rbf_pred = rbf.predict([[X, Y, Z, pitch, yaw, roll]])

        screen.fill(0)
        font = pygame.font.SysFont("calibri",40)
        text = font.render("Polynomial Kernel: " + poly_pred[0], True,(255,255,255))
        screen.blit(text,(50,50))
        
        font = pygame.font.SysFont("calibri",40)
        text = font.render("RBF Kernel: " + rbf_pred[0], True,(255,255,255))
        screen.blit(text,(50,100))
        pygame.display.flip()

        time.sleep(0.01)

X, y = getData()
poly, rbf = trainingAll(X,y)
joblib.dump(poly, 'poly.pkl')
joblib.dump(rbf, 'rbf.pkl')
#os.chdir(".\\data\\player0")
poly = joblib.load('poly.pkl')
rbf = joblib.load('rbf.pkl')
run(poly,rbf)





