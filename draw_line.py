from tkinter import *
from line import Line

class DrawLineCanvas(Canvas):
    # def __init__(self,window,width,height,color,row,column):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.bind("<Button-1>",self.draw_line)
        self.bind('<Motion>',self.show_mouse_pos)
        self.bind("<Button-3>",self.delete_line)
        self.click_num = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.old_x1 = 0
        self.old_y1 = 0
        self.drawn_ids = []
        self.label_id = 0
        self.lines = []

    def draw_line(self,event):
        if self.click_num == 0:
            self.x1=event.x
            self.y1=event.y
            self.click_num = 1
            # self.drawn_ids.append(self.create_oval(self.x1,self.y1,self.x1,self.y1,fill="black", width=5))
        else:
            self.x2=event.x
            self.y2=event.y
            self.drawn_ids.append(self.create_line(self.x1,self.y1,self.x2,self.y2,fill="black", width=2))
            # self.click_num = 0
            # print(f"just created line: {self.line_id}")
            self.addLine()
            self.x1=self.x2
            self.y1=self.y2
            # print(f"click_num: {self.click_num}")

    def delete_line(self,event):
        num_drawn = len(self.drawn_ids) 
        if num_drawn > 0:
            if num_drawn == 1:
                self.click_num = 0
                self.x1=0
                self.y1=0
            else:
                self.x1 = self.lines[-1][0][0]
                self.y1 = self.lines[-1][0][1]
            self.delete(self.drawn_ids.pop())
        if len(self.lines) > 0:
            self.lines.pop()
    
    def addLine(self):
        self.lines.append([[self.x1,self.y1],[self.x2,self.y2],self.getLen()])

    def getLen(self):
        return ((abs(self.x1-self.x2))**2+(abs(self.y1-self.y2))**2)**0.5

    def show_mouse_pos(self,event):
            x= event.x
            y= event.y
            # print(self.label_id)
            if self.label_id != 0:
                self.delete(self.label_id)
            
            self.label_id = self.create_text(100,100, font=("calibri", 20, "bold"),fill="black",text=f"X1: {x}\nY: {y}")
            # self.pack(expand=False)
            # print("Pointer is currently at %d, %d" %(x,y))