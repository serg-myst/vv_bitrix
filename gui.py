from tkinter import *
import tkinter as tk


class Gui(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="#FDF5E6")
        self.parent = parent
        self.parent.title("Задачи IT")
        self.parent.resizable(False, False)
        # self.pack(fill=BOTH, expand=1)
        # self.center_window()

    def center_window(self):
        w = 600
        h = 300

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    myLabel = Label(root, text='12445', pady=10)
    myLabel.pack()
    ex = Gui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
