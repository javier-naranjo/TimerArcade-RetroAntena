import keyboard
import os
import time
import configparser
import pygame
import subprocess
from pynput import keyboard as KEY
from threading import Thread
import pygetwindow as gw

pygame.mixer.init()
config = configparser.ConfigParser()
config.read('config.ini')
insertada = False
restante = 0
falta = 0
bloqueado = False
actual = 0
debounce = 0
ventanaOK = False
termino = True
minutos_moneda = int(config['RETROANTENA']['minutos'])
emu_conf = str(config['RETROANTENA']['emuladores'])
emuladores = emu_conf.split(',')
teclas = {"1", "2", "a", "s", "d", "z", "x", "c", "u", "i", "o", "j", "k", "l", "enter", "up arrow", "left arrow", "right arrow", "down arrow", "b", "n", "m", "h"}

###################################################################
def Hablar(txt):
    global actual
    print(txt)
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
def Bloquear():
    global bloqueado
    global teclas
    subprocess.call('"C:/MULTIJOGOS/ADVMENU/joytokey/JoyToKey.exe" -r "BLOQUE.cfg"', creationflags=0x08000000)
    for c in teclas:
        keyboard.remap_key(c,"g")
    bloqueado = True

###################################################################
def Desbloquear():
    global bloqueado
    global teclas
    if bloqueado:
        for c in teclas:
            keyboard.unhook_key(c)
        subprocess.call('"C:/MULTIJOGOS/ADVMENU/joytokey/JoyToKey.exe" -r "RASPBERRY PICO.cfg"', creationflags=0x08000000)
    bloqueado = False

#####################################################################
def Hide():
    global insertada
    global termino
    global falta
    global restante
    global debounce
    termino = False
    if time.time() > debounce + 0.2:
        insertada = True
        Desbloquear()
        falta = minutos_moneda + (restante / 60)
        restante = falta * 60
        Hablar("Te quedan " + str(int(falta)) + " minutos con " + str(int((falta % 1) * 60)) + " segundos   p")
        debounce = time.time()
    termino = True

###################################################################
def InsertaMoneda():
    global bloqueado
    global termino
    termino = False
    if bloqueado:
        Hablar("Inserta una moneda   p")
    termino = True

###################################################################
def ComprobarVentana():
    global emuladores
    global ventanaOK
    for coincidencia in emuladores:
        if coincidencia in gw.getActiveWindow().title:
            print("Ventana Activa")
        else:
            print("Realizando busqueda")
            for titulos in gw.getAllTitles():
                for coincidencia in emuladores:
                    if coincidencia in titulos:
                        win = gw.getWindowsWithTitle(coincidencia)[0]
                        win.restore()
                        win.activate()
                        ventanaOK = True
            break

###################################################################
class Loop(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global cont_monedas
        global insertada
        global restante
        global minutos_moneda
        global ventanaOK
        while True:
            if not ventanaOK:
                ComprobarVentana()
            if restante > 0:
                restante = restante - 1
            time.sleep(1)
            print(int(restante))
            if int(restante) % 10 == 0 and int(restante) <= 60 and int(restante) > 0:
                Hablar("Te quedan " + str(int(restante)) + " segundos   p")
            if insertada:
                if restante <= 0:
                    insertada = False
                    Bloquear()
                    cont_monedas = 0
                    Hablar("Tiempo terminado   p")
            else:
                continue

###################################################################
Loop()
Hablar("Estás usando el temporizador Retro Antena   p")
Bloquear()
ComprobarVentana()
for x in range(8):
    limpieza = "audio00" + str(x + 2) + ".wav"
    print(limpieza)
    if os.path.exists(limpieza):
            os.remove(limpieza)

with KEY.Events() as events:
    if termino:
        for event in events:
            if str(event) == "Press(key='5')":
                Hide()
            if str(event) == "Press(key='g')":
                InsertaMoneda()