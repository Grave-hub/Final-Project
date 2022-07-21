import turtle
import math

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

wn = turtle.Screen()
wn.title("Jumper")
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.bgcolor("beige")
wn.tracer(0)
wn.cv._rootwindow.resizable(False, False)

game_background = "final_project_cse210\game\casting\images\game_background.gif"
over_splash = "final_project_cse210\game\casting\images\game_over.gif"
kangaroo = "final_project_cse210\game\casting\images\kangaroo.gif"
car_right = "final_project_cse210\game\casting\images\car1.gif"
car_left = "final_project_cse210\game\casting\images\car2.gif"
river_log = "final_project_cse210\game\casting\images\log.gif"
volcano = "final_project_cse210\game\casting\images\\volcano.gif"

shapes = [kangaroo, car_right, car_left, river_log, volcano]
for shape in shapes:
    wn.register_shape(shape)

pen = turtle.Turtle()
pen.up()
pen.speed(0)
pen.hideturtle()

class Sprite():
    #sprite information
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
    #renders images
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()
    #update stuffs
    def update(self):
        pass
    #collision logic
    def is_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)
class Player(Sprite):
    #makes new player
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = 0
        self.collision = False
    #keyboard controls
    def up(self):
        self.y += 45
    def down(self):
        self.y -= 45
    def left(self):
        self.x -= 45
    def right(self):
        self.x += 45
    def update(self):
        self.x += self.dx
        if self.x < -270 or self.x > 270:
            self.x = 0
            self.y = -200
        elif self.y < -300:
            self.x = 0
            self.y = -200
#makes a car object
class Car(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
    def update(self):
        self.x -= self.dx
        if self.x < -300:
            self.x = 300
        if self.x > 300:
            self.x = -300
#makes a log object
class Logs(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
    def update(self):
        self.x += self.dx
        if self.x < -350:
            self.x = 300
        if self.x > 350:
            self.x = -300

player = Player(0, -200, 40, 40, kangaroo)
car_right = Car(0, -40, 40, 20, car_right, -0.2)
car_left = Car(0, -80, 40, 20, car_left, .2)
log_left = Logs(0, 200, 100, 40, river_log, .1)
log_right = Logs(0, 80, 100, 40, river_log, -.1)

goal1 = Sprite(0,250, 50, 50, volcano)

sprites = [car_left, car_right, log_left, log_right, goal1]
sprites.append(player)

wn.listen()
wn.onkeypress(player.up, "Up")
wn.onkeypress(player.down, "Down")
wn.onkeypress(player.left, "Left")
wn.onkeypress(player.right, "Right")

while True:
    pen.clear()
    game_state = "game"
    if game_state == "splash":
        wn.bgpic(over_splash)
    elif game_state == "game":
        wn.bgpic(game_background)
    for sprite in sprites:
        sprite.render(pen)
        sprite.update()

    player.dx = 0
    for sprite in sprites:
        if player.is_collision(sprite):
            if isinstance(sprite, Car):
                player.x = 0
                player.y = -200
                wn.clear
                game_state = "splash"
                break
            elif isinstance(sprite, Logs):
                player.dx = sprite.dx
                player.collision = True
                break
    if player.y > 80 and player.collision != True:
        player.x = 0
        player.y = -200
    wn.update()
    pen.clear()

