"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.

"""

from turtle import *
from random import randrange
from freegames import square, vector

food = vector(0, 0)
snake = [vector(0, 100)]
aim = vector(0, -10)

growCount = 0;
timerDelay = 200

def change(x, y):
    "Change snake direction."
    if ((x > 0 and aim.x < 0) or
        (x < 0 and aim.x > 0) or
        (y > 0 and aim.y < 0) or
        (y < 0 and aim.y > 0)):
        return
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190

def move():
    global timerDelay
    global growCount
    "Move snake forward one segment."
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head):
        if head.x >= 200:
            head.x = -190
        elif head.x <= -200:
            head.x = 190

        if head.y <= -200:
            head.y = 190
        elif head.y >= 200:
            head.y = -190

    if head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        growCount = 2
        if timerDelay > 50:
            timerDelay -= 10
        while True:
            food.x = randrange(-15, 15) * 10
            food.y = randrange(-15, 15) * 10
            if food not in snake and food != head:
                break

    if growCount <= 0:
        snake.pop(0)
    else:
        growCount -= 1

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'blue')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, timerDelay)

setup(420, 420, 0, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()
