"""
Update 1.5 20/06/2021

module antrian single server
author: Gregorius Guntur 311810015
        Benedictus Julian 311810007

"""
import pandas as pd
import time
# import threading
from random import randint
from collections import defaultdict
import numpy as np
import simpy
import tkinter as tk
from tkinter import *
import sys
from PIL import ImageTk

# Inisialisai Parameter
env = simpy.Environment()
capa = 1
server = simpy.Resource(env, capacity=capa)
n = 100 #Jumlah Pelanggan
ratadatang = 5 #jumlah waktu kedatangan

main = tk.Tk()
main.title("Pemodelan Simulasi")
canvas = tk.Canvas(main, width = 400, height = 100, bg = "white")
canvas.pack(side=tk.TOP, expand = False)
main.geometry("500x250")

"""
Model Simulasi
"""

def generate_datang():
    return random_generator(1).random_ekspon()
def generate_melayani():
    return random_generator(0.75).random_ekspon()

tunggu_t = []
list_t_datang = []
t_servis = []

def buka(env, server):
    i = 0
    while True:
        i += 1
        yield env.timeout(generate_datang())
        env.process(pelanggan(env, i, server))

def pelanggan(env,pembeli,server):
    with server.request() as request:
        t_datang = env.now
        list_t_datang.append(t_datang)
        langganan.add_to_line(1)
        print(env.now, 'Pelanggan {} datang'.format(pembeli))
        yield request
        t_servis.append(env.now)
        print (env.now, 'Pelanggan {} Dilayani'.format(pembeli))
        yield env.timeout(generate_melayani())
        print (env.now, 'Pelanggan {} Selesai dilayani'.format(pembeli))
        time.sleep(0.5)
        t_keluar = env.now
        langganan.remove_from_line(1)
        tunggu_t.append(t_keluar - t_datang)

obs_times = []
q_lenght = []

def observe(env, server):
    while True:
        obs_times.append(env.now)
        q_lenght.append(len(server.queue))
        yield env.timeout(1.0)




"""
Kelas Random Generater
"""
class QueueGraphics:
    text_height = 30
    icon_top_margin = -8

    def __init__(self, icon_file, icon_width, queue_name, num_lines, canvas, x_top, y_top):
        self.icon_file = icon_file
        self.icon_width = icon_width
        self.queue_name = queue_name
        self.num_lines = num_lines
        self.canvas = canvas
        self.x_top = x_top
        self.y_top = y_top

        self.image = tk.PhotoImage(file = self.icon_file)
        self.icons = defaultdict(lambda: [])
        for i in range(num_lines):
            canvas.create_text(x_top, y_top + (i * self.text_height), anchor = tk.NW, text = f"{queue_name} #{i + 1}")
        self.canvas.update()

    def add_to_line(self, seller_number):
        count = len(self.icons[seller_number])
        x = self.x_top + 60 + (count * self.icon_width)
        y = self.y_top + ((seller_number - 1) * self.text_height) + self.icon_top_margin
        self.icons[seller_number].append(
                self.canvas.create_image(x, y, anchor = tk.NW, image = self.image)
        )
        self.canvas.update()

    def remove_from_line(self, seller_number):
        if len(self.icons[seller_number]) == 0: return
        to_del = self.icons[seller_number].pop()
        self.canvas.delete(to_del)
        self.canvas.update()

def cost(canvas, x_top, y_top):
    return QueueGraphics("images/person-resized.gif", 25, "Kasir", capa ,canvas, x_top, y_top)

langganan = cost(canvas, 100, 20)

class random_generator():
    def __init__(self, beta):
        self.awalan = randint(0,1000)
        self.beta = beta
    def seedInit(self):
        global x
        x = self.awalan
        return x
    def LCG(self):
        a = 1140671485
        c = 128201163
        m = 2**24
        global x
        x = (a*x + c) % m
        return x
    def randomLCG(self):
        random_generator.seedInit(self)
        m = 2**24
        x = random_generator.LCG(self)
        r = x/m
        return r
    def random_ekspon(self):
        rand = random_generator.randomLCG(self)
        eks = -self.beta * np.log(1-rand)
        return eks

def runSimulation():
    env.process(buka(env,server))
    env.process(observe(env,server))
    env.run(until=10)





arrivalInput = tk.Entry(main,width=5)
serviceInput = tk.Entry(main,width=5)
serverInput = tk.Entry(main,width=5)

value_kedatangan=arrivalInput.get()
if value_kedatangan == "":
    f_value_kedatanan = 0.0
else:
    f_value_kedatanan = float(value_kedatangan)

value_pelayanan = serviceInput.get()
if value_pelayanan == "":
    f_value_pelayanan = 0.0
else:
    f_value_pelayanan = float(value_pelayanan)

runButton = Button(main, text="Run",command=runSimulation)
arrivalButton = Button(main, text="Enter arrival")
serviceButton = Button(main, text="Enter service")
serverButton = Button(main, text="Enter server")

arrivalInput.pack(side=tk.LEFT, padx=10)

arrivalButton.pack(side=tk.LEFT)

serviceInput.pack(side=tk.LEFT, padx = 10)

serviceButton.pack(side=tk.LEFT)

serverInput.pack(side=tk.LEFT,padx=10)
serverButton.pack(side=tk.LEFT)

runButton.pack(side=tk.TOP)
runButton.place(x=230, y=120)

main.mainloop()
#Membuat csv
x_waktu_tunggu = pd.Series(tunggu_t)
x_waktu_datang = pd.Series(list_t_datang)
#x_waktu_antri = pd.Series(obs_times)

stat_count = pd.DataFrame({
    "Waktu mengantri":x_waktu_tunggu,
    "waktu kedatangan":x_waktu_datang
})

stat_count.to_csv('se3_stat_count5.csv')

a = 0
dat = 0
i = 0
for u in list_t_datang:
    a+= u-dat
    dat = u
    i+=1

print(a/i)
print(np.mean(tunggu_t))

"""
import matplotlib.pyplot as plt

plt.hist(tunggu_t)
plt.xlabel("waktu menunggu")
plt.ylabel("jumlah pelanggan")

plt.figure()
plt.step(obs_times, q_lenght, where='post')
plt.xlabel('time min')
plt.ylabel('queue lenght')
plt.show()
"""
