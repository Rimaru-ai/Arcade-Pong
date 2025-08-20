# main.py
import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scorecard import Scorecard
from powerup import PowerUp
import random

# -----------------------
# Game Constants
# -----------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_MOVE_DISTANCE = 20
BALL_SPEED = 0.05
WIN_SCORE = 5  # optional win condition

# -----------------------
# Setup Screen
# -----------------------
screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

# -----------------------
# Game Objects
# -----------------------
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scorecard()
powerup = PowerUp()
powerup_timer = 0
active_effects = {"speed": 0, "shield": 0, "mega": 0}

# -----------------------
# Controls
# -----------------------
screen.listen()
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")
screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")
screen.onkeypress(screen.bye, "q")  # quit game with Q

# -----------------------
# Main Game Loop
# -----------------------
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # AI Opponent controls left paddle
    if ball.ycor() > l_paddle.ycor() + 10:
        l_paddle.go_up()
    elif ball.ycor() < l_paddle.ycor() - 10:
        l_paddle.go_down()

    # Power-up spawning
    powerup_timer += 1
    if powerup_timer > 500 and not powerup.isvisible():
        if random.random() < 0.02:  # 2% chance
            powerup.spawn()
            powerup_timer = 0

    # Check if ball collects powerup
    if powerup.isvisible() and ball.distance(powerup) < 20:
        effect = powerup.collect()
        if effect:
            active_effects[effect] = {
                "speed": 600,  # ~10 sec
                "shield": 2,  # 2 turns
                "mega": 4  # 4 turns
            }[effect]

    # Apply Speed Boost
    if active_effects["speed"] > 0:
        ball.move_speed = 0.03  # faster
        active_effects["speed"] -= 1
    else:
        ball.move_speed = 0.08  # reset to normal

    # Apply Shield
    if active_effects["shield"] > 0:
        if ball.xcor() > 380:  # right player has shield
            ball.bounce_x()
            active_effects["shield"] -= 1

    # Apply Mega Paddle
    if active_effects["mega"] > 0:
        r_paddle.shapesize(stretch_wid=7, stretch_len=1)
        active_effects["mega"] -= 1
    else:
        r_paddle.shapesize(stretch_wid=5, stretch_len=1)

    # Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with paddle
    if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or \
            (ball.distance(l_paddle) < 50 and ball.xcor() < -320):
        ball.bounce_x()

    # Detect right paddle miss
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # Detect left paddle miss
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

    # Optional: End game if someone wins
    if scoreboard.l_score == WIN_SCORE or scoreboard.r_score == WIN_SCORE:
        scoreboard.game_over()
        game_is_on = False

screen.mainloop()
