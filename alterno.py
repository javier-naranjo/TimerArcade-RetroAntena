import keyboard
from playsound import playsound
import os
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
insertada = False
unaVez = True
bloqueado = False
time_start = 0
cont_monedas = 0
minutos_moneda = int(config['RETROANTENA']['minutos'])
teclas = {"a", "s", "d", "z", "x", "c", "u", "i", "o", "j", "k", "l"}

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

###################################################################
def InsertaMoneda():
    try:
        print(os.path.join(os.getcwd(), "moneda.wav"))
        playsound(os.path.join(os.getcwd(), "moneda.wav"))
    except Exception as e:
        print("problema Sonido")

###################################################################
keyboard.add_hotkey('5', Hide)
keyboard.add_hotkey('1', InsertaMoneda)
keyboard.add_hotkey('2', InsertaMoneda)
keyboard.add_hotkey('enter', InsertaMoneda)
keyboard.add_hotkey('esc', Cerrar)
Bloquear()

while True:
    restante = (time_start + (cont_monedas * minutos_moneda * 60)) - time.time()
    time.sleep(0.9)
    if int(restante) % 10 == 0 and int(restante) <= 60 and int(restante) > 0:
        InsertaMoneda()
    if insertada:
        if time.time() > time_start + (cont_monedas * minutos_moneda * 60):
            insertada = False
            Bloquear()
            cont_monedas = 0
        else:
            print(restante)
    else:
        continue