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

# Define snake as a dictionary of information
snake1 = {
    'body': [vector(0, 100)],
    'nextAim': vector(0, 10), # Remember the keypress to process on next loop
    'aim': vector(0, 10),
    'colour': 'blue'
}

snake2 = {
    'body': [vector(0, -100)],
    'nextAim': vector(0, -10),
    'aim': vector(0, -10),
    'colour': 'orange'
}

snakes = [snake1, snake2] # Create a list of snakes

timerDelay = 200 # time until the next loop

def change(x, y, snake):
    """Record a direction change request."""
    nextAim = vector(x,y)
    if validMove(nextAim, snake): # Only set to new direction if it's a valid move
        # Store until the update loop so we can validate multiple inputs during a frame
        snake['nextAim'] = nextAim

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
    snake['aim'] = snake['nextAim'] # Set next move to current direction
    head.move(snake['aim']) # Move the head
    wrap(head) # Wrap the head position around the edge of the play area

    if head in occupiedSquares:
        return True # If head collided then return with collided = True
    else:
        snake['body'].append(head) # Else attached head to body and return collided = False
        return False

def moveSnakes():
    """Move the snakes and update game state"""
    global timerDelay

    # Create list of squares snakes cannot run into
    occupiedSquares = []
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
            if timerDelay > 0: # Increase the speed of the game
                timerDelay -= 5
            while True: # Place new food
                food.x = randrange(-15, 15) * 10
                food.y = randrange(-15, 15) * 10
                if food not in occupiedSquares: # Ensure food is not on an occupied square
                    break
        else:
            # Since we added the head we need to trim the tail
            # So we don't keep growing
            snake['body'].pop(0)

    return False # Return False to say we didn't collide with anything

def drawSnakes():
    """Draw the snakes and food onto the screen"""
    clear()
    for snake in snakes:
        for body in snake['body']:
            square(body.x, body.y, 9, snake['colour'])

    square(food.x, food.y, 9, 'green')
    update()

def updateGame():
    """Update the game state."""
    global timerDelay

    collided = moveSnakes()
    if collided:
        return # End game if snakes collided
    drawSnakes()

    ontimer(updateGame, timerDelay) # Call this function again after the timerDelay

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
