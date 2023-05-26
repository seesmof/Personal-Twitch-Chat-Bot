import tkinter


def show_popup():
    root = tkinter.Tk()
    popup = tkinter.Toplevel(root)
    tkinter.Label(popup, text="Hello World").pack()
    root.after(5000, popup.destroy)
    root.mainloop()


show_popup()

for i in range(100):
    print(i)
