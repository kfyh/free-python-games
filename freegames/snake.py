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
snake1 = {
    'body': [vector(0, 100)],
    'aim': vector(0, 10),
    'recordedMoves': [],
    'growCount': 0,
    'colour': 'blue'
}

snake2 = {
    'body': [vector(0, -100)],
    'aim': vector(0, -10),
    'recordedMoves': [],
    'growCount': 0,
    'colour': 'yellow'
}

snakes = [snake1, snake2]

timerDelay = 200

def change(x, y, snake):
    """Record a direction change request."""
    if len(snake['recordedMoves']) < 2:
        snake['recordedMoves'].append(vector(x, y))

def wrap(head):
    """Wrap the head around the play area."""
    if head.x >= 200:
        head.x = -190
    elif head.x <= -200:
        head.x = 190

    if head.y <= -200:
        head.y = 190
    elif head.y >= 200:
        head.y = -190

def validMove(nextMove, snake):
    """Check with the next move does not move back into the snake."""
    return not ((nextMove.x > 0 and snake['aim'].x < 0) or
            (nextMove.x < 0 and snake['aim'].x > 0) or
            (nextMove.y > 0 and snake['aim'].y < 0) or
            (nextMove.y < 0 and snake['aim'].y > 0))

def moveHead(head, snake, occupiedSquares):
    """Move the head of the snake."""
    nextMove = snake['aim'] # Set next move to current direction
    if len(snake['recordedMoves']) > 0: # If a change is recorded, set next move to change of direction
        changeMove = snake['recordedMoves'].pop(0)
        if validMove(changeMove, snake): # Only set to new direction if it's a valid move
            nextMove = changeMove

    head.move(nextMove) # Move the head
    snake['aim'] = nextMove # Set new head direction
    wrap(head) # Wrap the head position around the edge of the play area

    if head in occupiedSquares:
        return True # If head collided then return with collided = True
    else:
        snake['body'].append(head) # Else attached head to body and return collided = False
        return False

def moveSnakes():
    global timerDelay
    """Move the snakes and update game state"""
    # Create list of squares snakes cannot run into
    occupiedSquares = [];
    for snake in snakes:
        occupiedSquares += snake['body']

    # Loop through the snakes to update their position
    for snake in snakes:
        head = snake['body'][-1].copy()
        # Move the head and check if it collided with anything
        collided = moveHead(head, snake, occupiedSquares)
        if collided:
            # End the game if it collided
            square(head.x, head.y, 9, 'red')
            update()
            return True

        # Add the head to the list of forbidden squares
        occupiedSquares.append(head)

        # Check if snake ate the food
        if head == food:
            snake['growCount'] = 2 # If eaten the food, we will grow by 2 squares
            if timerDelay > 0: # Increase the speed of the game
                timerDelay -= 5
            while True: # Place new food
                food.x = randrange(-15, 15) * 10
                food.y = randrange(-15, 15) * 10
                if food not in occupiedSquares: # Ensure food is not on an occupied square
                    break

        if snake['growCount'] <= 0:
            snake['body'].pop(0)
        else:
            snake['growCount'] -= 1
    return False

def drawSnakes():
    """Draw the snakes and fod onto the screen"""
    clear()
    for snake in snakes:
        for body in snake['body']:
            square(body.x, body.y, 9, snake['colour'])
    
    square(food.x, food.y, 9, 'green')
    update()

def updateGame():
    """Update the game state."""
    global timerDelay

    if moveSnakes():
        return
    drawSnakes()

    ontimer(updateGame, timerDelay)

setup(420, 420, 0, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0, snake1), 'Right')
onkey(lambda: change(-10, 0, snake1), 'Left')
onkey(lambda: change(0, 10, snake1), 'Up')
onkey(lambda: change(0, -10, snake1), 'Down')
onkey(lambda: change(10, 0, snake2), 'd')
onkey(lambda: change(-10, 0, snake2), 'a')
onkey(lambda: change(0, 10, snake2), 'w')
onkey(lambda: change(0, -10, snake2), 's')
updateGame()
done()
