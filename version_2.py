import sys
import cv2
import numpy as np
import time
import imutils

# Function for stereo vision and depth estimation
import triangulation as tri 
import calibration
import get_image as get

# Mediapipe for face detection << not use
import time
import data as DB

arduino = serial.Serial('/dev/ttyACM0', 9600) # serial port set

# object declare and reset
class object:
    def __init__(self, name, x, y, z, w, h):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.distance = 0
    def dis(self,):
        
        self.distance = np.sqrt((self.x)**2 + (self.y)**2 + (self.z)**2) 
        print(self.distance)

def reset(class_list):
    for index in range(0, len(class_list)-1): # range()에 class_list의 index가 올 수 있도록
        class_list[index]= object("None", 0, 0, 0, 0, 0 )
        class_list[index].distance = 0

def data_swap(list):
    for i in range(0, len(list)-1):
         for j in range(0,len(list)):     
            if class_list[j].x < class_list[i].x : 
                class_list[j],class_list[i] = class_list[i],class_list[j]

######################### yolo ##################################### 

net = cv2.dnn.readNet("yolov3_training_version2.weights", "yolov3_testing.cfg")
classess = []
with open("obj.names", "r") as f :
    classess = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

############################################################################################

# Stereo vision setup parameters << need to check what camera's spec is correct
frame_rate = 60    #Camera frame rate (maximum at 120 fps)
B = 8               #Distance between the cameras [cm]
f = 8              #Camera lense's focal length [mm]
alpha = 70        #Camera field of view in the horisontal plane [degrees]

# storage declare
left_class_list = [ object for n in range(26)]
reset(left_class_list)
right_class_list = [ object for n in range(26)]
reset(right_class_list)
final_class_list = [ object for n in range(26)]
reset(final_class_list)
value = [0,0,0,0,0]
########################## Main program loop  ###############################
num=2

while True:
    #################### get and set image ##############################################
    get.image(num)
    imgL = cv2.imread("/home/pi/Documents/images/stereoLeft/imageL2.png")
    imgR = cv2.imread("/home/pi/Documents/images/stereoLeft/imageL2.png")

    succes_right, frame_right = imgR
    succes_left, frame_left = imgL

    ################## CALIBRATION #########################################################

    frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)

    ########################################################################################

        # If cannot catch any frame, break
    if not succes_right.any() or not succes_left.any():  # error occured
        print("not exist image")
        break

    else:

        ################ yolo ##############
        right_height, right_width, _ = frame_right.shape
        left_height, left_width, _ = frame_left.shape

        # Detecting objects in frame_left

        blob_left = cv2.dnn.blobFromImage(frame_left, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob_left)
        Louts = net.forward(output_layers)
            
        # manufacturing proper object data from left frame detecting ouput
        Lclass_ids = []
        Lconfidences = []
        Lboxes = []
        for out in Louts:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.1:
                    # Object detected
                    Lcenter_x = int(detection[0] * Lwidth) 
                    Lcenter_y = int(detection[1] * Lheight) 
                    Lw = int(detection[2] * Lwidth)
                    Lh = int(detection[3] * Lheight)
                    
                    Lx = int(Lcenter_x - Lw / 2)
                    Ly = int(Lcenter_y - Lh / 2)
                    Lboxes.append([Lx, Ly, Lw, Lh])
                    Lconfidences.append(float(confidence))
                    Lclass_ids.append(class_id)
        Lindexes = cv2.dnn.NMSBoxes(Lboxes, Lconfidences, 0.5, 0.4) # delete noise

        font = cv2.FONT_HERSHEY_PLAIN
        Lcolors = np.random.uniform(0, 255, size=(len(Lboxes), 3))
        for i in range(len(Lboxes)):
            if i in Lindexes:
                Lx, Ly, Lw, Lh = Lboxes[i]
                label = str(classess[Lclass_ids[i]])
                color = Lcolors[i]
                ####################### store left output  #############################################
                if label == "clamper":
                    print("clamper")
                else :
                    left_class_list[i]=object(label, Lx+ Lw/2, Ly + Lh/2, 0, Lw, Lh)
                #############################################################################
                
                ########################## display on the monitor ############################
                cv2.rectangle(frame_left, (Lx, Ly), (Lx + Lw, Ly + Lh), color, 2)
                cv2.putText(frame_left, label, (Lx, Ly + 30), font, 3, color, 3)

                ###########################################################################
                
        # Detecting objects in frame_right

        blob_right = cv2.dnn.blobFromImage(frame_right, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob_right)
        Routs = net.forward(output_layers)
            
        # manufacturing proper object data from right frame detecting ouput
        Rclass_ids = []
        Rconfidences = []
        Rboxes = []
        for out in Routs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.1:
                    # Object detected
                    Rcenter_x = int(detection[0] * Rwidth)
                    Rcenter_y = int(detection[1] * Rheight) 
                    Rw = int(detection[2] * Rwidth)
                    Rh = int(detection[3] * Rheight)
                    
                    Rx = int(Rcenter_x - Rw / 2)
                    Ry = int(Rcenter_y - Rh / 2)
                    Rboxes.append([Rx, Ry, Rw, Rh])
                    Rconfidences.append(float(confidence))
                    Rclass_ids.append(class_id)
        Rindexes = cv2.dnn.NMSBoxes(Rboxes, Rconfidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        Rcolors = np.random.uniform(0, 255, size=(len(Rboxes), 3))
        for i in range(len(Rboxes)):
            if i in Rindexes:
                Rx, Ry, Rw, Rh = Rboxes[i]
                label = str(classess[Rclass_ids[i]])
                color = Rcolors[i]
                ####################### store right output  #############################################
                if label == "clamper":
                    print("clamper")
                else :
                    right_class_list[i]= object(label, Rx + Rw/2, Ry + Rh/2, 0, Rw, Rh)
                #############################################################################
                
                ########################## display on the monitor ############################
                cv2.rectangle(frame_right, (Rx, Ry), (Rx + Rw, Ry + Rh), color, 2)
                cv2.putText(frame_right, label, (Rx, Ry + 30), font, 3, color, 3)
         

            ################## CALCULATING DEPTH, Storing calculating output, Finding prior data and display #########################################################
        # object
        for i in range(0, len(left_class_list)-1):
            if left_class_list[i].name == right_class_list[i].name:
                Ob_x, Ob_y, Ob_z = tri.find_coordination(left_class_list[i].x, left_class_list[i].y, right_class_list[i].x, right_class_list[i].y, frame_right, frame_left, B, f, alpha)
                final_class_list[i] = object(left_class_list[i].name, Ob_x, Ob_y, Ob_z, left_class_list[i].w, left_class_list[i].h)
                 
            else :
                print("left not right ")
        
        # swap function run
        data_swap(final_class_list)
        value = DB.motor(final_class_list[0].name, final_class_list[0].x, final_class_list[0].y, final_class_list[0].z, final_class_list[0].w)
        cv2.imshow("frame right", frame_right) 
        cv2.imshow("frame left", frame_left)

#######################################################################################################################################
        print("communication start")

        # data send
        b = bytearray(value)
        arduino.write(b)
        
        # data recevice
        while True:
            msg = arduino.readline()
            print(msg)
            ack = int(msg[:-2].decode())
            print(ack)
            if ack == 1:
                print("communication finish")
                break
        
#######################################################################################################################################

        # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ##################### prepare next case ###############
        cv2.destroyAllWindows()
        reset(left_class_list)
        reset(right_class_list)
        reset(final_class_list)
        value = [0.0.0.0.0]


# Release and destroy all windows before termination
cv2.destroyAllWindows()
