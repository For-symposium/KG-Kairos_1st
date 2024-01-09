from turtle import *
import time

size = 1
angle = 0
pen_state = True
is_shift_pressed = False


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

def forward():
    t.forward(10)

def backward():
    t.backward(10)

def turn_left():
    global angle
    angle += 10
    t.left(angle)

def turn_right():
    global angle
    angle -= 10
    t.right(angle)

def clear_all():
    t.up()
    t.clear()
    t.home()
    t.down()

def pensize_up():
    global size
    size += 1
    t.pensize(size)
    print("Pen size up")

def pensize_down():
    global size
    if (size > 1):
        size -= 1
        t.pensize(size)
        print("Pen size down")

def pen_updown():
    global pen_state
    if (pen_state): # true -> false
        t.up()
        pen_state = not pen_state
        print("Pen state : ", pen_state)
    else: # false -> true
        t.down()
        pen_state = not pen_state
        print("Pen state : ", pen_state)

scr = Screen()
t = Turtle()
scr.title("My screen")
scr.listen()


scr.listen()
scr.onkeypress(forward, 'Up')
scr.onkeypress(backward, 'Down')
scr.onkeypress(turn_left, 'Left')
scr.onkeypress(turn_right, 'Right')
scr.onkeypress(clear_all, 'c')
scr.onkeypress(pensize_up, "]")
scr.onkeypress(pensize_down, "[")
scr.onkeypress(pen_updown, "p")
scr.onkeypress(t.undo, "z")
