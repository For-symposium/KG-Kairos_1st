from turtle import *
import time

def rectangle(row, col):
    forward(row)
    left(90)
    forward(col)
    left(90)
    forward(row)
    left(90)
    forward(col)
    left(90)

def gt(pos1, pos2):
    pu()
    goto(pos1, pos2)
    pd()

scr = Screen()
t = Turtle()

# scr.listen()
# scr.onkeypress(rectangle(30, 30), 'UP')
# gt(-100, -100)
# scr.onkeypress(rectangle(10, 10), 'DOWN')
def func(size):
    print(size)


time.sleep(2)