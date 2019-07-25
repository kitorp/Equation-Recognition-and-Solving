# TrainAndTest.py

import cv2
import numpy as np
import operator
import os

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################
class ContourWithData():

    # member variables ############################################################################
    npaContour = None           # contour
    boundingRect = None         # bounding rect for contour
    intRectX = 0                # bounding rect top left corner x location
    intRectY = 0                # bounding rect top left corner y location
    intRectWidth = 0            # bounding rect width
    intRectHeight = 0           # bounding rect height
    fltArea = 0.0               # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA: return False
        return True

###################################################################################################
def main():
    allContoursWithData = []
    validContoursWithData = []

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)
    except:
        print "error, unable to open classifications.txt, exiting program\n"
        os.system("pause")
        return
    # end try

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
    except:
        print "error, unable to open flattened_images.txt, exiting program\n"
        os.system("pause")
        return
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

    kNearest = cv2.ml.KNearest_create()

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    imgTestingNumbers = cv2.imread("testfinal.png")

    if imgTestingNumbers is None:
        print "error: image not read from file \n\n"
        os.system("pause")
        return
    # end if

    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)       # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur


    #cv2.imshow("Without Blur" , imgGray);
    #cv2.imshow("Blurred" , imgBlurred);
                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean

    imgThreshCopy = imgThresh.copy()

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,
                                                 cv2.RETR_EXTERNAL,         # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)   # compress horizontal, vertical, and diagonal segments and leave only their end points

    for npaContour in npaContours:                             # for each contour
        contourWithData = ContourWithData()                                             # instantiate a contour with data object
        contourWithData.npaContour = npaContour                                         # assign contour to contour with data
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
        allContoursWithData.append(contourWithData)                                     # add contour with data object to list of all contours with data
    # end for

    for contourWithData in allContoursWithData:
        if contourWithData.checkIfContourIsValid():
            validContoursWithData.append(contourWithData)
        # end if
    # end for

    validContoursWithData.sort(key = operator.attrgetter("intRectX"))

    strFinalString = ""
    length=0
    hash_ache=False
    for contourWithData in validContoursWithData:

        cv2.rectangle(imgTestingNumbers,
                      (contourWithData.intRectX, contourWithData.intRectY),     # upper left corner
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),      # lower right corner
                      (0, 255, 0),              # green
                      2)                        # thickness

        imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,     # crop char out of threshold image
                           contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array

        npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)

        strCurrentChar = str(chr(int(npaResults[0][0])))
        if strCurrentChar=='#':
            hash_ache=True
        if(hash_ache==False and strCurrentChar=='-'):
            strCurrentChar='I'

        strFinalString = strFinalString + strCurrentChar
        length+=1
    # end for

    print "\n" + strFinalString + "\n"
    num = 0
    ans = 0
    if strFinalString[0]=='#':
        S = strFinalString
        n = len(S)
        tp = []
        i = 1
        while (i < n):
            if (S[i] == '+'):
                tp.append(-100001)
            elif (S[i] == '-'):
                tp.append(-100002)
            elif (S[i] == '*'):
                tp.append(-100003)
            elif (S[i] == '/'):
                tp.append(-100004)
            else:
                x = 0
                ix = i
                while (ix < n and (S[ix] >= '0' and S[ix] <= '9' or S[ix] == 'O' or S[ix] == 'o')): ix += 1
                for j in range(i, ix):
                    y = S[j]
                    if (S[j] == 'O' or S[j] == 'o'): y = '0'
                    x = x * 10 + ord(y) - 48
                tp.append(x)
                # print(i)
                i = ix - 1
                # print(i)
            i += 1
        # print (tp)
        sv = []

        i = 1
        # print("done")
        sv.append(tp[0])
        # print(sv)

        while (i < len(tp)):
            if (tp[i] == -100004):
                x = sv.pop()
                y = tp[i + 1]
                sv.append(x / y)

            else:
                sv.append(tp[i])
                sv.append(tp[i + 1])
            # print(sv)
            i += 2
        # print("here")

        if len(sv) > 0: tp = sv
        # print (tp)
        sv = []

        i = 1

        sv.append(tp[0])

        while (i < len(tp)):
            if (tp[i] == -100003):
                x = sv.pop()
                y = tp[i + 1]
                sv.append(x * y)

            else:
                sv.append(tp[i])
                sv.append(tp[i + 1])
            i += 2

        if len(sv) > 0: tp = sv
        # print (tp)
        sv = []
        i = 1

        sv.append(tp[0])

        while (i < len(tp)):
            if (tp[i] == -100002):
                x = sv.pop()
                y = tp[i + 1]
                sv.append(x - y)

            else:
                sv.append(tp[i])
                sv.append(tp[i + 1])
            i += 2

        if len(sv) > 0: tp = sv
        # print (tp)
        sv = []
        i = 1

        sv.append(tp[0])

        while (i < len(tp)):
            if (tp[i] == -100001):
                x = sv.pop()
                y = tp[i + 1]
                sv.append(x + y)

            else:
                sv.append(tp[i])
                sv.append(tp[i + 1])
            i += 2
        if len(sv) > 0: tp = sv
        #print (tp)
        print "The answer is : %d " % tp[0]

    cv2.imshow("imgTestingNumbers", imgTestingNumbers)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    return

###################################################################################################
if __name__ == "__main__":
    main()
# end if