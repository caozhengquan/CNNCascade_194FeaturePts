import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
import os
#resize image to 'resizeTo'
def resizeRate(h,resizeTo = 800.0):
    return float(resizeTo/h)

#select a point to move
def find_closest_pts(x,y,thresh = 10.0):
    imin = -1
    dmin = -1
    for i in range(0,194):
        distance = pow(pow(point[2*i + 0] - x,2) + pow(point[2*i + 1] - y,2),0.5)
        if imin < 0 or distance < dmin:
            imin = i
            dmin = distance
    if dmin >= 0 and dmin < thresh:
        return imin
    else:
        return -1

#use mouse control points position
def mv_MouseCallback(event,x,y,flags,param):
    global pidx, point
    if event == cv2.EVENT_LBUTTONDOWN:
        if pidx < 0:
            pidx = find_closest_pts(x,y)
            if pidx != -1:
                print "Selected point is : " + str(pidx)
        else:
            pidx = -1
        img = cleanimg.copy()
    elif event == cv2.EVENT_MOUSEMOVE:
        if pidx >= 0:
            point[2*pidx + 0] = float(x)
            point[2*pidx + 1] = float(y)
            img = cleanimg.copy()


#set the image and points
def setImage(filename):
    fid = open(filename,'r')
    imagename = fid.readline().strip()
    origin_img = cv2.imread("./helen_data/" + imagename + ".jpg")
    print "dealing with image : " + imagename + ".jpg"
    #resize the image
    rate = resizeRate(origin_img.shape[0])
    origin_img = cv2.resize(origin_img,(int(origin_img.shape[1]*rate),int(origin_img.shape[0]*rate)))
    point = np.zeros((194*2,))
    
    for i in range(0,194):
        line = fid.readline()
        words = line.split(" , ")
        point[2*i + 0] = float(words[0])*rate
        point[2*i + 1] = float(words[1].strip())*rate
    
    fid.close()
    return imagename,origin_img,point,rate

#save points position
def savePointsPosition(image,point,rate,filename):
    os.system("rm " + filename)
    fid = open(filename,'w')
    fid.write(image + "\n")
    for i in range(0,194):
        fid.write(str(point[2*i + 0] / rate) + " , " + str(point[2*i + 1] / rate) + "\n")
    print "save " + filename

if __name__ =="__main__":
    
    imagerange = 2331
    i = input("start image is : ")
    while(1):
        txtfile = "./annotation/" + str(i) + ".txt"
        cv2.namedWindow("image")
        cv2.setMouseCallback("image",mv_MouseCallback)
        pidx = -1
        imagename,img,point,rate = setImage(txtfile)
        
        #set up for clean image
        cleanimg = img.copy()
        outputTxt = "ESC: break  Q: front image  W: next image"
        cv2.putText(cleanimg,
                    outputTxt,
                    (0,30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,(255,255,255))
        outputTxt = str(i) + ".txt"
        cv2.putText(cleanimg,
                    outputTxt,
                    (0,60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,(255,255,255))
                    #quit
        quit = False
        while(1):
            img = cleanimg.copy()
            for pts in range(0,194):
                cv2.circle(img,(int(point[2*pts + 0]),int(point[2*pts + 1])),1,(255,0,0))
            cv2.imshow("image",img)
            #quit
            k = cv2.waitKey(100)
            if k == 27:
                savePointsPosition(imagename,point,rate,txtfile)
                cv2.destroyAllWindows()
                quit = True
                break
            #front image
            elif k == 113 and i > 1:
                i = i - 1
                print "front image"
                savePointsPosition(imagename,point,rate,txtfile)
                cv2.destroyAllWindows()
                break
            #next image
            elif k == 119 and i < imagerange:
                i = i + 1
                print "next image"
                savePointsPosition(imagename,point,rate,txtfile)
                cv2.destroyAllWindows()
                break
            #do nothing
            else:
                continue

        #if ESC was pressed
        if quit == True:
            print "quit"
            break
        else:
            continue
