"""defining a track:
    Desired Track: Simple Oval
    Define straight segments of equal length (10m)
    
    
    
    
    

"""

import numpy as np
import cv2

class Oval_Track:
    
    def __init__(self,name,filepath,total_length,units):
        self.name = name
        self.filepath = filepath
        self.total_length = total_length
        self.units = units
        self.track_color = self.setTrackColor()
        self.im = self.readInTrack(filepath)
        self.imgray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)


    def readInTrack(self, track_filepath):
        im = cv2.imread(track_filepath)
        return im

    def getTrackCoords(self):
        # ret, thresh = cv2.threshold(self.imgray, 127, 255, 0)
        X,Y = np.where(np.all(self.im==self.track_color,axis=2))

        print(X,Y)

    def setTrackColor(self):
        hasCustomColor = input("Custom color? Default is black. [Y/N]")
        if hasCustomColor == "Y":
            rval = input("Input R value:")
            gval = input("Input G value:")
            bval = input("Input B value:")
            self.track_color = [rval,gval,bval]
        else:
            self.track_color = [0,0,0]
    
    def displayImage(self, cv2_im):
        cv2.imshow("image",cv2_im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def main():
        oval_track = Oval_Track("Oval Track","Tracks\Simple Oval\Simple Oval.JPG","839.78","meters")
    if __name__ == '__main__':
        main()