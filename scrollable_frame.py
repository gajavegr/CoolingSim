import tkinter as tk
from tkinter import *
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
        def __init__(self, container, *args, **kwargs):
            super().__init__(container, *args, **kwargs)
            canvas = tk.Canvas(self)
            
            scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

            scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

            self.scrollable_frame = ttk.Frame(canvas)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")