import turtle
import random
import time

delay=0.1
sc=0
hs=0
bodies=[]

#crating a screen
s=turtle.Screen()
s.title("Snake Game")
s.bgcolor("light blue")
s.setup(width=600,height=600) #Size of Screen

#Creating a Head
head=turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("blue")
head.fillcolor("red")
head.penup()
head.goto(0,0)
head.direction="stop"

#Creating Food For Snake
food=turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.fillcolor("blue")
food.penup()
food.ht() #for Hiding a Turtle
food.goto(150,200)
food.st() #for Showing a turtle

#Creating Score Board
sb=turtle.Turtle()
sb.penup()
sb.ht()
sb.goto(-250,250)
sb.write("Score:0 | Highest Score:0") # to print a score on the screen for the 1st time.

# Creating Function for moving in all directions.
def moveUP():
    if head.direction!="down"
       head.direction="up"
def moveDown():
    if head.direction!="up"
        head.direction="down"
def moveRight():
    if head.direction!="left"
        head.direction="right"
def moveLeft():
    if head.direction!="right"
        head.direction="left"
