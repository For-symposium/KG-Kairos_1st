# turtle contents 전부 가져와서 tt.~~ 할 필요 없어짐
from turtle import *
import turtle as tt
import time

def draw_square(length, thick):
    tt.pensize(thick)
    tt.forward(length)
    tt.left(90)
    tt.forward(length)
    tt.left(90)
    tt.forward(length)
    tt.left(90)
    tt.forward(length)

def rectangle(row, col):
    forward(row)
    left(90)
    forward(col)
    left(90)
    forward(row)
    left(90)
    forward(col)
    left(90)

def draw_tri(length, thick):
    tt.forward(length)
    tt.left(120)
    tt.forward(length)
    tt.left(120)
    tt.forward(length)
    
# my_tt = tt.Turtle() # 독립된 개체 만들기, For the other purpose
# my_tt.screen.bgcolor("aqua")
# my_tt.penup()
# my_tt.hideturtle()
# my_tt.goto(-100, -10)
# my_tt.write("Hi my_tt", True, align='left', font=('', 20, ''))
# my_tt.pendown()

tt.speed(100)

# tt.fillcolor("blue")
# tt.begin_fill()
# tt.shape("turtle")
# tt.color("green","red")
# draw_square(100, 5)
# tt.goto(0,100)
# tt.left(90)
# draw_tri(100, 5)
# tt.end_fill()

def draw_circle(pos, rad, color='', thick=''):
    if (thick):
        tt.pensize(thick)
    tt.penup()
    tt.goto(pos)
    tt.pendown()
    if (color):
        tt.color(color)
    tt.circle(rad)

def draw_olympic():
    draw_circle((0,0), 45, "black", 5)
    draw_circle((100, 0), 45, "red", 5)
    draw_circle((-100, 0), 45, "blue", 5)
    draw_circle((-50, -50), 45, "yellow", 5)
    draw_circle((50, -50), 45, "green", 5)

def gt(pos1, pos2):
    pu()
    goto(pos1, pos2)
    pd()

gt(-300, -120)
rectangle(600, 280)

arr1 = ['ESC', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'LCK']
for i in range(14):
    gt(-300+40*(i+1)-10, 100)
    rectangle(28, 23)
    gt(-300+40*(i+1)-3, 105)
    write(arr1[i])

arr2 = ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", '0', '-', '=', 'Del']
for i in range(14):
    gt(-300+40*(i+1)-10, 65)
    rectangle(28, 23)
    gt(-300+40*(i+1)-3, 70)
    write(arr2[i])

arr3 = ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|']
for i in range(14):
    gt(-300+40*(i+1)-10, 30)
    rectangle(28, 23)
    gt(-300+40*(i+1)-3, 35)
    write(arr3[i])

arr4 = ['CAP', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', 'ENT']
for i in range(12):
    gt(-300+40*(i+1)-10, -5)
    rectangle(28, 23)
    gt(-300+40*(i+1)-3, 0)
    write(arr4[i])
gt(210, -5)
rectangle(70, 23)
gt(220, 0)
write(arr4[12])

arr5 = ['SHT', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', 'SHT']
gt(-270, -40)
rectangle(60, 23)
gt(-260, -35)
write(arr5[0])
for i in range(10):
    gt(-300+40*(i+3)-10, -40)
    rectangle(28, 23)
    gt(-300+40*(i+3)-3, -35)
    write(arr5[i+1])
gt(217, -40)
rectangle(60, 23)
gt(227, -35)
write(arr5[11])

arr6 = ['FN', 'CTR', 'OPT', 'CMD', 'SPACE', 'CMD', 'OPT']
for i in range(4):
    gt(-300+40*(i+1)-10, -75)
    rectangle(28, 23)
    gt(-300+40*(i+1)-3, -70)
    write(arr6[i])
gt(-300+40*(4+1)-10, -75)
rectangle(160, 23)
gt(-300+40*(4+2)+10, -70)
write(arr6[4])
for i in range(2):
    gt(-300+40*(i+9)+10, -75)
    rectangle(28, 23)
    gt(-300+40*(i+9)+17, -70)
    write(arr6[i+5])
for i in range(3):
    gt(-300+40*(i+11)+20, -75)
    rectangle(28, 8)
gt(-300+40*12+20, -62)
rectangle(28, 8)

time.sleep(2)

