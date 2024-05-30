from turtle import Screen, Turtle
from PIL import Image
import random
import sys

# Set up the screen
screen = Screen()
screen.title("Car Parking Game")
screen.bgcolor("white")
screen.setup(width=600, height=400)

# Resize images using Pillow
car_image = Image.open("car.gif")
car_image = car_image.resize((50, 30))  # Adjust the size as needed
car_image.save("car_resized.gif", "GIF")

parking_image = Image.open("parking.gif")
parking_image = parking_image.resize((50, 30))  # Adjust the size as needed
parking_image.save("parking_resized.gif", "GIF")

# Register GIF images for car and parking rectangle
screen.addshape("car_resized.gif")
screen.addshape("parking_resized.gif")

# Create the car
car = Turtle()
car.shape("car_resized.gif")
car.penup()

# Create the parking rectangle
parking_rectangle = Turtle()
parking_rectangle.shape("parking_resized.gif")
parking_rectangle.penup()
parking_rectangle.setposition(random.randint(-250, 250), random.randint(-150, 150))

# Score variable
score = 0

# Function to move the car left
def move_left():
    x = car.xcor()
    if x > -290:
        car.setx(x - 10)

# Function to move the car right
def move_right():
    x = car.xcor()
    if x < 290:
        car.setx(x + 10)

# Function to move the car up
def move_up():
    y = car.ycor()
    if y < 190:
        car.sety(y + 10)

# Function to move the car down
def move_down():
    y = car.ycor()
    if y > -190:
        car.sety(y - 10)

# Function to exit the game
def exit_game():
    screen.bye()

# Check if the car is inside the parking rectangle
def check_parking():
    global score
    car_x, car_y = car.position()
    rect_x, rect_y = parking_rectangle.position()

    if (
        rect_x - 20 < car_x < rect_x + 20
        and rect_y - 10 < car_y < rect_y + 10
    ):
        # Car is in the rectangle, move to the next level
        parking_rectangle.setposition(random.randint(-250, 250), random.randint(-150, 150))
        score += 1
        update_score()

# Function to update the score display
def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Arial", 12, "normal"))

# Keyboard bindings
screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(exit_game, "Escape")

# Exit button turtle
exit_button = Turtle()
exit_button.hideturtle()
exit_button.penup()
exit_button.color("red")
exit_button.goto(250, 180)
exit_button.write("Exit", align="center", font=("Arial", 12, "normal"))
exit_button.onclick(exit_game)

# Score display turtle
score_display = Turtle()
score_display.hideturtle()
score_display.penup()
score_display.color("black")
score_display.goto(0, 180)
score_display.write(f"Score: {score}", align="center", font=("Arial", 12, "normal"))

# Main game loop
try:
    while True:
        check_parking()
        screen.update()
except Exception:
    pass
