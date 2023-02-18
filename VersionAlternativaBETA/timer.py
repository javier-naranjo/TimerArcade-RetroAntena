from tkinter import *
from PIL import ImageTk, Image
from screeninfo import get_monitors

##################################################################################
root = Tk()
resolucion = str(get_monitors()[0].width) + "x" + str(get_monitors()[0].height)
root.geometry(resolucion)
frame = Frame(root, width=get_monitors()[0].width, height=get_monitors()[0].height)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
if get_monitors()[0].width == 320:
    img = ImageTk.PhotoImage(Image.open("moneda_320.png"))
elif get_monitors()[0].width == 640:
    img = ImageTk.PhotoImage(Image.open("moneda_640.png"))
elif get_monitors()[0].width == 800:
    img = ImageTk.PhotoImage(Image.open("moneda_800.png"))
elif get_monitors()[0].width == 1280:
    img = ImageTk.PhotoImage(Image.open("moneda_1280.png"))
else:
    img = ImageTk.PhotoImage(Image.open("moneda_1920.png"))
label = Label(frame, image = img)
label.pack()

root.title('timer')
root.wm_attributes('-fullscreen', 'True')
root.wm_attributes('-topmost', '1')
mainloop()