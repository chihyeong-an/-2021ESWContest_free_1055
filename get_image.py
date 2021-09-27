import cv2

def image(num):

    cap = cv2.VideoCapture(0)


    _,img = cap.read()
    height, width, _ = img.shape

    # devided idea
    frame_left = img[0:height, 0:int(width/2)].copy()
    frame_right = img[0:height, int(width/2):width].copy()
    # print(height, width/2)
    # print(width - int(width)/2)
    
    img_l = frame_left
    img_r = frame_right

    cv2.imwrite('/home/pi/Documents/images/stereoLeft/imageL' + str(num) + '.png', img_l)
    cv2.imwrite('/home/pi/Documents/images/stereoright/imageR' + str(num) + '.png', img_r)
    print("images saved!")
    # cv2.imshow("frame", img)

    cap.release()
    cv2.destroyAllWindows()
    
#image(1)
