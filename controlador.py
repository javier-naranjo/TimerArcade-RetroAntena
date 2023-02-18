import keyboard
from ahk import AHK
from playsound import playsound
import os
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
insertada = False
unaVez = True
time_start = 0
cont_monedas = 0
minutos_moneda = int(config['RETROANTENA']['minutos'])
ahk = AHK()
os.system("TASKKILL /F /IM timer.exe")
os.startfile('"' + os.getcwd() + "/timer.exe" + '"')
win = None

while win == None:
    time.sleep(0.25)
    win = ahk.win_get(title='timer')
    #win = ahk.find_window_by_text(b"timer.exe")
print(win)


###################################################################
def Cerrar():
    os.system("TASKKILL /F /IM timer.exe")
    os._exit(0)

###################################################################
def Show():
    global win
    win.activate()
    win.maximize()
    win.restore()
    win.show()
    win.to_top()

###################################################################
def Hide():
    global insertada
    global time_start
    global cont_monedas
    global win
    insertada = True
    time_start = time.time()
    cont_monedas = cont_monedas + 1
    print(time_start)
    win.to_bottom() 

###################################################################
def InsertaMoneda():
    try:
        print(time.time())
        playsound(os.path.join(os.getcwd(), "moneda.wav"))
    except Exception as e:
        print("problema Sonido")

###################################################################
keyboard.add_hotkey('a', InsertaMoneda)
keyboard.add_hotkey('s', InsertaMoneda)
keyboard.add_hotkey('d', InsertaMoneda)
keyboard.add_hotkey('z', InsertaMoneda)
keyboard.add_hotkey('x', InsertaMoneda)
keyboard.add_hotkey('c', InsertaMoneda)
keyboard.add_hotkey('u', InsertaMoneda)
keyboard.add_hotkey('i', InsertaMoneda)
keyboard.add_hotkey('o', InsertaMoneda)
keyboard.add_hotkey('j', InsertaMoneda)
keyboard.add_hotkey('k', InsertaMoneda)
keyboard.add_hotkey('l', InsertaMoneda)
keyboard.add_hotkey('1', Show)
keyboard.add_hotkey('5', Hide)
keyboard.add_hotkey('esc', Cerrar)

while True:              
    if insertada:
        if time.time() > time_start + (cont_monedas * minutos_moneda * 60):
            insertada = False
            Show()
            cont_monedas = 0
        else:
            print(time.time() - (time_start + (cont_monedas * minutos_moneda * 60)))
            time.sleep(1)
    else:
        continue