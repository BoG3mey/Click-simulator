import tkinter as tk
from pynput import keyboard
import json
import os
import pyautogui

select = 0
SpeedOfMoveing = 0
active = 0

def on_press(key): 
    global active
    try:
        if key == keyboard.Key.ctrl_r:
            if active == 0:
                active = 1
                change_position()
        if key == keyboard.Key.alt_gr:
            show_position()
        print('Key {} pressed.'.format(key.char))
    except AttributeError:
        print('Special key {} pressed.'.format(key))

def change_position():
    global active

    if select == 0:
        pass
    else:
        for i in range(len(data[select])):
            x = data[select][i][0]
            y = data[select][i][1]
            b = data[select][i][2]
            BonusButton = data[select][i][3]
            if b == 'left' or b == 'right':
                pyautogui.click(x, y, button = b, duration = SpeedOfMoveing)
            elif b == 'none':
                pass
            elif b == 'shift':
                    pyautogui.keyDown('shift')
                    pyautogui.click(x, y, button = BonusButton, duration = SpeedOfMoveing + 0.2)
                    pyautogui.click(x, y, button = BonusButton, duration = SpeedOfMoveing)
                    pyautogui.keyUp('shift')
            else:
                if BonusButton == 'none':
                    pyautogui.moveTo(x, y, duration = SpeedOfMoveing)
                    pyautogui.press(b)
        active = 0    

def on_scale_change(val):
    global SpeedOfMoveing
    SpeedOfMoveing = float(val) / 100

def show_position():
    if select != 0:
        position = pyautogui.position()
        data[select].append([position.x, position.y, 'none', 'none'])
        with open(filepath, 'w') as file:
            json.dump(data, file)

def on_select(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    global select
    select = keys[index]

filename = "config.json"
filepath = os.path.join(os.path.dirname(__file__), filename)
with open(filepath) as file:
    data = json.load(file)

root = tk.Tk()
root.geometry("200x150")



# Start listener
listener = keyboard.Listener(on_press=on_press)
listener.start()




scale = tk.Scale(root, from_= 0, to = 100, command=on_scale_change, font=("Arial", 20), length=150)
scale.pack(side="right", anchor="nw")

lb = tk.Listbox(root, height=10)
lb.pack(side="left", anchor="ne")

# Получаем все ключи из словаря и добавляем их в Listbox
keys = list(data.keys())
for key in keys:
    lb.insert("end", key)

lb.bind("<<ListboxSelect>>", on_select)

root.resizable(False, False)
root.mainloop()