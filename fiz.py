import pygame
import math
from collections import namedtuple

class Point:
   def __init__(self, x, y):
       self.x = x
       self.y = y
class Scalar:
   def __init__(self, c):
       self.c = c

pygame.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)
width = 1500
height = 900
screen_res = (width, height)
k = 25 # Stala Coulomba
delta = 0.1
screen = pygame.display.set_mode(screen_res)


red = (255, 50, 50)
blue = (50, 50, 255)
white = (200, 200, 200)

ball1radius = Scalar(40)
ball2radius = Scalar(40)
ball1mass = Scalar(1)
ball2mass = Scalar(1)
ball1_obj = Point(200.0, 500.0)
ball2_obj = Point(800.0, 300.0)
F = Point(0, 0)
ball1_obj_v = Point(0.0, 0.0)
ball2_obj_v = Point(0.0, 0.0)

charge1 = Scalar(0)
charge2 = Scalar(0)

def restart(scenario = 0):
    print("restarting")
    ball1_obj_v.x = 0.0
    ball1_obj_v.y = 0.0

    ball2_obj_v.x = 0.0
    ball2_obj_v.y = 0.0

    charge1.c = 0
    charge2.c = 0

    ball1_obj.x = 200.0
    ball1_obj.y = 500.0

    ball2_obj.x = 800.0
    ball2_obj.y = 300.0

    ball1mass.c = 1
    ball1mass.c = 1
    ball1radius.c = 40

    if scenario==1:
        ball1_obj_v.x = 0.0
        ball1_obj_v.y = -1.0

        ball2_obj_v.x = 0.0
        ball2_obj_v.y = 1.0

        ball1_obj.x = 800.0
        ball2_obj.x = 1200.0

        charge1.c = 3
        charge2.c = -3
    elif scenario==2:
        ball1_obj.x = 700.0
        ball2_obj.x = 850.0

        ball1_obj.y = 500.0
        ball2_obj.y = 500.0

        charge1.c = 10
        charge2.c = 10
    elif scenario==3:
        ball1mass.c = 20
        ball1radius.c = 100

        ball2_obj_v.y = 2.5

        ball1_obj.x = 800.0
        ball2_obj.x = 1150.0
        ball2_obj.y = 400.0
        ball1_obj.y = 400.0

        charge1.c = 3
        charge2.c = -3


restart()

pause = False

while True:

    events = pygame.event.get()
    for event in events: #dodawanie ladunkow przez strzalki

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and charge1.c > -10:
                charge1.c -= 1
            if event.key == pygame.K_RIGHT and charge1.c < 10:
                charge1.c += 1
            if event.key == pygame.K_UP and charge2.c < 10:
                charge2.c += 1
            if event.key == pygame.K_DOWN and charge2.c > -10:
                charge2.c -= 1
            if event.key == pygame.K_r:
                restart()
            if event.key == pygame.K_1:
                restart(1)
            if event.key == pygame.K_2:
                restart(2)
            if event.key == pygame.K_3:
                restart(3)
            if event.key == pygame.QUIT:
                exit()
            if event.key == pygame.K_SPACE:
                pause = not pause
                if pause:
                    print("PAUSED")
                    print("c",charge1.c, charge2.c)
                    print("d",xdistance,' ',ydistance)
                    print("b1",ball1_obj.x,' ',ball1_obj.y)
                    print("b2",ball2_obj.x,' ',ball2_obj.y)
                    print("v1",ball1_obj_v.x,ball1_obj_v.y)
                    print("v2",ball2_obj_v.x,ball2_obj_v.y)
                    print("f",f)
                    print("fy",F.y)
                    print("fx",F.x)
                    print("r",r)
                    print("f/r",f/r)

    if not pause:
        if math.hypot(ball1_obj.x - ball2_obj.x, ball1_obj.y - ball2_obj.y) <= ball1radius.c + ball2radius.c: #zderzenie
            ball1_obj_v.x = 0
            ball2_obj_v.x = 0
            ball1_obj_v.y = 0
            ball2_obj_v.y = 0
        else:
            ball1_obj.x += ball1_obj_v.x * delta
            ball1_obj.y += ball1_obj_v.y * delta
            ball2_obj.x += ball2_obj_v.x * delta
            ball2_obj.y += ball2_obj_v.y * delta

            if ball1_obj.x - ball1radius.c <= 0 or ball1_obj.x + ball1radius.c >= width:
                ball1_obj_v.x = -ball1_obj_v.x
            if ball1_obj.y - ball1radius.c <= 0 or ball1_obj.y + ball1radius.c >= height:
                ball1_obj_v.y = -ball1_obj_v.y

            if ball2_obj.x - ball2radius.c <= 0 or ball2_obj.x + ball2radius.c>= width:
                ball2_obj_v.x = -ball2_obj_v.x
            if ball2_obj.y - ball2radius.c<= 0 or ball2_obj.y + ball2radius.c>= height:
                ball2_obj_v.y = -ball2_obj_v.y

        if charge1.c >= 0:
            charge1.csymbol = "+"
        else:
            charge1.csymbol = ""

        if charge2.c >= 0:
            charge2.csymbol = "+"
        else:
            charge2.csymbol = ""

        c1 = charge1.c
        c2 = charge2.c
        xdistance = ball2_obj.x - ball1_obj.x
        ydistance = ball2_obj.y - ball1_obj.y
        rsquare = xdistance * xdistance + ydistance * ydistance
        f = k * (c1 * c2 / rsquare) #wzor Coulomba
        r = math.sqrt(rsquare)

        F.x = f/r * xdistance
        F.y = f/r * ydistance

        ball2_obj_v.x += F.x / ball2mass.c
        ball2_obj_v.y += F.y / ball2mass.c
        ball1_obj_v.x += -F.x / ball1mass.c
        ball1_obj_v.y += -F.y / ball1mass.c

        #rysowanie na ekranie
        screen.fill(white)
        pygame.draw.circle(surface=screen, color=red,center=[int(ball1_obj.x), int(ball1_obj.y)], radius=ball1radius.c)
        pygame.draw.circle(surface=screen, color=blue,center=[int(ball2_obj.x), int(ball2_obj.y)], radius=ball2radius.c)
        ball1chargetext = my_font.render(charge1.csymbol + str(charge1.c), False, (0, 0, 0))
        ball2chargetext = my_font.render(charge2.csymbol + str(charge2.c), False, (0, 0, 0))
        screen.blit(ball1chargetext, (ball1_obj.x-12,ball1_obj.y-21))
        screen.blit(ball2chargetext, (ball2_obj.x-12,ball2_obj.y-21))


        pygame.display.flip()
