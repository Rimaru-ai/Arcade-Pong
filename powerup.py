from turtle import Turtle
import random

# -----------------------
# Constants
# -----------------------
POWERUP_TYPES = ["speed", "shield", "mega"]
POWERUP_COLORS = {"speed": "red", "shield": "blue", "mega": "green"}

class PowerUp(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_wid=1, stretch_len=1)
        self.penup()
        self.hideturtle()
        self.type = None

    def spawn(self):
        """Spawn random powerup at random location"""
        self.type = random.choice(POWERUP_TYPES)
        self.color(POWERUP_COLORS[self.type])
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        self.goto(x, y)
        self.showturtle()

    def collect(self):
        """When collected, disappear"""
        self.hideturtle()
        return self.type
