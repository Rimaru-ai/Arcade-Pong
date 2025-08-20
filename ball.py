from turtle import Turtle

# -----------------------
# Constants
# -----------------------
INITIAL_MOVE_SPEED = 0.08   # slower update cycle
SPEED_INCREMENT = 0.95      # smaller speed increase each hit


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 4
        self.y_move = 4
        self.move_speed = INITIAL_MOVE_SPEED

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= SPEED_INCREMENT  # increase difficulty

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = INITIAL_MOVE_SPEED
        self.bounce_x()
