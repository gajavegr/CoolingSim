"""defining a track:
    Description: select an image and connect dots to make a track of segments with corneres on apexes
    Usage: readTrack_interactive.py -t <input_file> -l <track_length_in_meters> -o <output_file>
        left click to start adding lines
        right click to undo/delete last line added
        type keyboard "s" when ready to save to csv
"""

import cv2
import tkinter as tk
from tkinter import *
import sys, getopt
from PIL import ImageTk,Image
import csv
from scrollable_frame import ScrollableFrame
from draw_line import DrawLineCanvas

class Track:
    
    def __init__(self,name,image_filepath,output_filepath,total_length):
        self.name = name
        self.track_image = image_filepath
        self.output_filepath = output_filepath
        self.total_length = float(total_length)
        self.background_color = "white"
        self.im = self.readInTrack()
        self.track_lines = []

    def readInTrack(self):
        return cv2.imread(self.track_image)

    def drawTrackPoints(self):
        height, width, channels = self.im.shape
        root= tk.Tk()
        # root.geometry(f"{width}x{height}")
        frame = ScrollableFrame(root)
        
        canvas = DrawLineCanvas(frame.scrollable_frame,width=1200,height=800,background=self.background_color)
        # canvas=Canvas(frame.scrollable_frame, width=width, height=height, background=self.background_color)
        # canvas.pack()
        canvas.grid(row=0, column=0)
        img = ImageTk.PhotoImage(Image.open(self.track_image))
        canvas.create_image(20, 20, anchor=NW, image=img) 
        
        frame.pack(side="left", fill="both", expand=True)
        
        self.track_lines = canvas.lines

        def saveToCSV(event):
            if(event.char == "s"):
                self.writeLinesToCSV()

        root.bind("<Key>",saveToCSV)
            
        root.mainloop()
    
    def writeLinesToCSV(self):
        fields = ["x1","y1","x2","y2","len","len in meters"]
        rows = []
        total_xy_len = sum(line[2] for line in self.track_lines)
        for line in self.track_lines:
            scale = self.total_length/total_xy_len #meters/pixel
            actual_len = line[2]*scale #pixels * (meters/pixel) = meters ✔
            rows.append([line[0][0],line[0][1],line[1][0],line[1][1],line[2],actual_len])

        with open(self.output_filepath, 'w', newline='') as csvfile: 
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

def main():
    argv = sys.argv[1:]

    input_file = ''
    output_file = ''
    track_length = 0
    try:
        opts, args = getopt.getopt(argv,"t:o:l:")
    except getopt.GetoptError:
        print('readTrack_interactive.py -t <input_file> -l <track_length_in_meters> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ["-t"]:
            input_file = arg
        elif opt in ["-o"]:
            output_file = arg
        elif opt in ["-l"]:
            track_length = arg
    print(f"Track image file is {input_file}")
    print(f"Output file is {output_file}")
    print(f"Track length is {track_length}")
    oval_track = Track("Oval Track",input_file,output_file,track_length)
    oval_track.drawTrackPoints()


if __name__ == '__main__':
    main()