import keyboard
import os
import time
import configparser
import pygame

pygame.mixer.init()
config = configparser.ConfigParser()
config.read('config.ini')
insertada = False
restante = 0
unaVez = True
bloqueado = False
time_start = 0
cont_monedas = 0
minutos_moneda = int(config['RETROANTENA']['minutos'])
teclas = {"a", "s", "d", "z", "x", "c", "u", "i", "o", "j", "k", "l", "enter"}

###################################################################
def Hablar(txt):
    try:
        pygame.mixer.music.unload()
        if os.path.exists("audio001.wav"):
            os.remove("audio001.wav")
        f = open("texto.txt","w+")
        f.write(txt)
        f.close()
        os.system('ejecutar.cmd')
        pygame.mixer.music.load("audio001.wav")
        pygame.mixer.music.play()
    except Exception as e:
        print(e)

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
    try:
        Hablar("Inserta una moneda   p")
    except Exception as e:
        print("problema Sonido")

###################################################################
keyboard.add_hotkey('5', Hide)
keyboard.add_hotkey('esc', Cerrar)
keyboard.add_hotkey('2', InsertaMoneda)
keyboard.add_hotkey('1', InsertaMoneda)
Bloquear()

while True:
    restante = (time_start + (cont_monedas * minutos_moneda * 60)) - time.time()
    time.sleep(0.9)
    if int(restante) % 10 == 0 and int(restante) <= 60 and int(restante) > 0:
        Hablar("Te quedan " + str(int(restante)) + " segundos")
    if insertada:
        if time.time() > time_start + (cont_monedas * minutos_moneda * 60):
            insertada = False
            Bloquear()
            cont_monedas = 0
        else:
            print(int(restante))
    else:
        continue