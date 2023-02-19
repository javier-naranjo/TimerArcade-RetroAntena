import keyboard
import os
import time
import configparser
import pygame
import subprocess
from pynput import keyboard as KEY
from threading import Thread

pygame.mixer.init()
config = configparser.ConfigParser()
config.read('config.ini')
insertada = False
restante = 0
unaVez = True
bloqueado = False
time_start = 0
actual = 0
cont_monedas = 0
minutos_moneda = int(config['RETROANTENA']['minutos'])
teclas = {"1", "2", "a", "s", "d", "z", "x", "c", "u", "i", "o", "j", "k", "l", "enter", "up arrow", "left arrow", "right arrow", "down arrow", "b", "n", "m", "h"}

###################################################################
def Hablar(txt):
    global actual
    if time.time() > actual: 
        try:
            pygame.mixer.music.unload()
            if os.path.exists("audio001.wav"):
                os.remove("audio001.wav")
            f = open("texto.txt","w+")
            f.write(txt)
            f.close()
            subprocess.call('"C:/Program Files (x86)/Loquendo/LTTS7/bin/TTSFileGenerator.exe" -v Jorge -q -o audio "texto.txt"', creationflags=0x08000000)
            while not os.path.exists("audio001.wav"):
                print("Aun no")
            time.sleep(0.15)
            pygame.mixer.music.load("audio001.wav")
            pygame.mixer.music.play()
        except Exception as e:
            print(e)
        actual = time.time()

###################################################################
def Cerrar():
    keyboard.unhook_all()
    os._exit(0)

###################################################################
def Bloquear():
    global bloqueado
    global teclas
    for c in teclas:
        keyboard.remap_key(c,"g")
    for c in teclas:
        keyboard.release(c)
    bloqueado = True

###################################################################
def Desbloquear():
    global bloqueado
    global teclas
    for c in teclas:
        if bloqueado:
            keyboard.unhook_key(c)
    bloqueado = False

###################################################################
def Hide():
    global insertada
    global time_start
    global cont_monedas
    insertada = True
    time_start = time.time()
    cont_monedas = cont_monedas + 1
    Desbloquear()
    falta = int((((time_start + (cont_monedas * minutos_moneda * 60)) - time.time()) + 10) / 60)
    Hablar("Te quedan " + str(falta) + " minutos   p")
    print("Te quedan " + str(falta) + " minutos")

###################################################################
def InsertaMoneda():
    global bloqueado
    if bloqueado:
        Hablar("Inserta una moneda   p")

###################################################################
class Loop(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global cont_monedas
        global insertada
        global time_start
        global restante
        global minutos_moneda
        while True:
            restante = (time_start + (cont_monedas * minutos_moneda * 60)) - time.time()
            time.sleep(0.9)
            if int(restante) % 10 == 0 and int(restante) <= 60 and int(restante) > 0:
                Hablar("Te quedan " + str(int(restante)) + " segundos   p")
            if insertada:
                if time.time() > time_start + (cont_monedas * minutos_moneda * 60):
                    insertada = False
                    Bloquear()
                    cont_monedas = 0
                    Hablar("Tiempo terminado   p")
                else:
                    print(int(restante))
            else:
                continue

###################################################################
Loop()
#keyboard.add_hotkey('5', Hide)
#keyboard.add_hotkey('esc', Cerrar)
Bloquear()

with KEY.Events() as events:
    for event in events:
        if event.key == KEY.Key.esc:
            Cerrar()
        if str(event) == "Press(key='5')":
            Hide()
        if str(event) == "Press(key='g')":
            InsertaMoneda()
