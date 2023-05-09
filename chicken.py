from turtle import *
from threading import Thread
import tkinter as tk
from time import sleep
from config import *
from os import remove
from random import *
from tqdm import tqdm
try:
    remove('score.json')
except FileNotFoundError:
    pass
try:
    score_file = open("score.json", "w")
except FileNotFoundError:
    score_file = open("score.json", "x")
saved_score = "{}"
cached_score = 0
game_over = False
screen = Screen()
player = Turtle()
score = Turtle()
score.hideturtle()
score.speed(0)
score.pu()
score.setpos(400, 350)
chicken_shape = Shape("image", tk.PhotoImage(file="chicken.png"))
addshape("chicken", chicken_shape)
egg_shape = Shape("image", tk.PhotoImage(file="egg.png"))
addshape("egg", egg_shape)
player.shape("chicken")
zombie_shape = Shape("image", tk.PhotoImage(file="zombie_chicken.png"))
addshape("zombie", zombie_shape)
dezombie_shape = Shape("image", tk.PhotoImage(file="dezombie_chicken.png"))
addshape("dezombie", dezombie_shape)
eggs = []
screen.bgcolor("#00FFFF")
player.pu()
player.forward(10)
player.speed(0)
class DummyTurtle():
    def pu():
        pass
    def speed(*args): 
        pass
    def shape(*args):
        pass
    def setpos(*args):
        pass
def refresh_chickens():
    for i in tqdm(eggs):
        if i["new"] == True:
            make_setup_egg(i)()
            i["new"] = False
def layegg():
    new_egg = {"turtle":Turtle(),"create":"Turtle","time":0,"x":player.xcor(),"y":player.ycor(),"hatched":False,"moved":0,"zombie":False,"dezombie":False,"dezombie_target":None,"targeted":False,"new":True}
    eggs.append(new_egg)
    refresh_chickens()
    ##Thread(target=make_setup_egg(new_egg),daemon=True).start()
def hatch_egg(egg, chick_type):
    def start_egg(x, y):
        egg["hatched"] = True
        if chick_type == 1:
            egg["zombie"] = True
            egg["turtle"].shape("zombie")
        elif chick_type == 0:
            egg["turtle"].shape("chicken")
        else:
            egg["dezombie"] = True
            egg["turtle"].shape("dezombie")
    return start_egg
def make_setup_egg(egg):
    def setup_egg():
        egg["turtle"].pu()
        egg["turtle"].speed(0)
        egg["turtle"].shape("egg")
        egg["turtle"].setpos(egg["x"], egg["y"])
        egg["turtle"].onclick(hatch_egg(egg, 0), 1)
        egg["turtle"].onclick(hatch_egg(egg, 2), 2)
        egg["turtle"].onclick(hatch_egg(egg, 1), 3)
    return setup_egg
def calculate_fps():
    if 1/fps < 1:
        return 1/fps
    else:
        return 0

def loop():
    while True:
        sleep(calculate_fps()*10)
        if not len(eggs) == 0:
            global i
        global cached_score
        if not len(eggs) == cached_score:
            score.clear()
            cached_score = len(eggs)
            score.write(cached_score,font=("Arial",20,"normal"))
        if game_over:
            break
def hatch_chickens():
    while True:
        for j in eggs:
            if j["hatched"] and not j["moved"]>1500 and not j["zombie"] and not j["dezombie"]:
                j["turtle"].setx(j["turtle"].xcor()-10)
                j["moved"] += 10
        sleep(calculate_fps())
def save_score():
    saved_score = str("{" + "'" + score_name + "'" + ":{'eggs':" + str(eggs) + '}' + '}')
    score_file.write(saved_score)
def incubate_eggs():
    while True:
        sleep(randint(0, 5))
        with eggs[randint(0, len(eggs)-1)] as i:
            if i["time"] == fps*3:
                i["hatched"] = True
def zombie_chicken_ai():
    while True:
        for i in eggs:
            if i["zombie"]:
                if player.xcor() > i["turtle"].xcor():
                    i["turtle"].setx(i["turtle"].xcor()+zombie_speed)
                elif player.xcor() < i["turtle"].xcor():
                    i["turtle"].setx(i["turtle"].xcor()-zombie_speed)
                elif player.ycor() > i["turtle"].ycor():
                    i["turtle"].sety(i["turtle"].ycor()+zombie_speed)
                elif player.ycor() < i["turtle"].ycor():
                    i["turtle"].sety(i["turtle"].ycor()-zombie_speed)
        sleep(calculate_fps())
def dezombie_chicken_ai():
    while True:
        for i in eggs:
            if i["dezombie"]:
                for index, zombie  in enumerate(eggs):
                    if zombie["targeted"]:
                        continue
                    if zombie["zombie"] and i["dezombie_target"] == None:
                        i["dezombie_target"] = index
                        zombie["targeted"] = True
                if eggs[index]["turtle"].xcor() > i["turtle"].xcor():
                    i["turtle"].setx(i["turtle"].xcor()+zombie_speed)
                elif eggs[index]["turtle"].xcor() < i["turtle"].xcor():
                    i["turtle"].setx(i["turtle"].xcor()-zombie_speed)
                elif eggs[index]["turtle"].ycor() > i["turtle"].ycor():
                    i["turtle"].sety(i["turtle"].ycor()+zombie_speed)
                elif eggs[index]["turtle"].ycor() < i["turtle"].ycor():
                    i["turtle"].sety(i["turtle"].ycor()-zombie_speed)
        sleep(calculate_fps())
def start_chickens_loop():
    return
def reset_game():
    screen.clearscreen()
    screen.bgcolor("cyan")
    player=Turtle()
    eggs = []
    screen.onkeypress(lambda:player.setx(player.xcor()-10), "Left")
    screen.onkeypress(lambda:player.setx(player.xcor()+10), "Right")
    screen.onkeypress(lambda:player.sety(player.ycor()+10), "Up")
    screen.onkeypress(lambda:player.sety(player.ycor()-10), "Down")
    screen.onkeypress(layegg, "space")
    screen.onkeypress(save_score, "Escape")
    screen.onkeypress(reset_game, "r")
    player.shape("chicken")
    player.pu()
                        
                
        
screen.onkeypress(lambda:player.setx(player.xcor()-10), "Left")
screen.onkeypress(lambda:player.setx(player.xcor()+10), "Right")
screen.onkeypress(lambda:player.sety(player.ycor()+10), "Up")
screen.onkeypress(lambda:player.sety(player.ycor()-10), "Down")
screen.onkeypress(layegg, "space")
screen.onkeypress(save_score, "Escape")
screen.onkeypress(reset_game, "r")
screen.listen()
Thread(target=hatch_chickens, daemon=True).start()
Thread(target=loop, daemon=True).start()
Thread(target=zombie_chicken_ai, daemon=True).start()
Thread(target=dezombie_chicken_ai, daemon=True).start()
Thread(target=start_chickens_loop,daemon=True).start()

try:
    screen.mainloop()
except Exception:
    print('GAME CRASHEDred[0m')
game_over = True

score_file.close()
