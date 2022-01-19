import time
from turtle import Turtle, Screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_HALF_HEIGHT = int(SCREEN_HEIGHT / 2)
SCREEN_HALF_WIDTH = int(SCREEN_WIDTH / 2)
BORDER = 30
PADDLE_TURTLE_DIMENSION = 20
SLEEP_DURATION = 0.01
INITIAL_X_DISPLACEMENT = 1
INITIAL_Y_DISPLACEMENT = 0.5
SCOREBOARD_WIDTH = 100

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color("white")
        self.goto(0, 0)
        self.x_displacement = INITIAL_X_DISPLACEMENT
        self.y_displacement = INITIAL_Y_DISPLACEMENT
        self.x = self.xcor()
        self.y = self.ycor()

    def move(self):
        self.x += self.x_displacement
        self.y += self.y_displacement
        self.goto(x=int(self.x), y=int(self.y))

    def reflect_horizontally(self):
        self.x_displacement = -self.x_displacement

    def reflect_vertically(self):
        self.y_displacement = -self.y_displacement

    def hit_horizontal_borders(self):
        if self.ycor() >= (SCREEN_HALF_HEIGHT - BORDER - PADDLE_TURTLE_DIMENSION/2) or self.ycor() <= (-SCREEN_HALF_HEIGHT + BORDER + PADDLE_TURTLE_DIMENSION/2):
            return True
        else:
            return False

    def stop(self):
        self.x_displacement = 0
        self.y_displacement = 0

    def increase_speed(self):
        self.x_displacement *= 1.1
        self.y_displacement *= 1.1
        pass




class Paddle:
    def __init__(self, xcor, ycor):
        # The x and y co-ordinate refer to the top most block
        self.xcor = xcor
        self.ycor = ycor
        self.segments = []
        for i in range(3):
            new_turtle = Turtle()
            new_turtle.color("white")
            new_turtle.shape("square")
            new_turtle.penup()
            new_turtle.goto(x=xcor, y=ycor)
            self.segments.append(new_turtle)
            ycor -= PADDLE_TURTLE_DIMENSION

    def move_up(self):
        # print("Moving up")
        if self.segments[0].ycor() <= SCREEN_HALF_HEIGHT - BORDER:
            for segment in self.segments:
                y_cor = segment.ycor()
                segment.sety(y_cor + PADDLE_TURTLE_DIMENSION)

    def move_down(self):
        # print("Moving down")
        if self.segments[-1].ycor() >= -SCREEN_HALF_HEIGHT + BORDER:
            for segment in self.segments:
                y_cor = segment.ycor()
                segment.sety(y_cor - PADDLE_TURTLE_DIMENSION)
                print(segment.ycor())

    def hit(self, ball):
        x_cor = self.segments[0].xcor()
        if abs(x_cor - ball.xcor()) <= PADDLE_TURTLE_DIMENSION and (self.segments[0].ycor() + PADDLE_TURTLE_DIMENSION) >= ball.ycor() >= (self.segments[-1].ycor() - PADDLE_TURTLE_DIMENSION):
            return True
        else:
            return False

class ScoreBoard:
    def __init__(self):
        self.scores = [0, 0]
        self.turtle = Turtle()
        self.turtle.color("white")
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.goto(x=int(-SCOREBOARD_WIDTH/2), y=SCREEN_HALF_HEIGHT - BORDER)
        self.refresh()



    def increment1(self):
        self.scores[0] += 1
        self.refresh()

    def increment2(self):
        self.scores[1] += 1
        self.refresh()

    def refresh(self):
        self.turtle.clear()
        message = str(self.scores[0]) + "          :          " + str(self.scores[1])
        self.turtle.write(arg=message, font=("Arial", 24, "bold"))
        pass


class Pong:
    pass

    def __init__(self):
        # Create screen as a member variable and initialize it
        self.screen = Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Pong")
        self.screen.tracer(0)
        self.paddles = []
        new_paddle = Paddle(-SCREEN_HALF_WIDTH + BORDER, SCREEN_HALF_HEIGHT)
        self.paddles.append(new_paddle)
        new_paddle = Paddle(SCREEN_HALF_WIDTH-BORDER, SCREEN_HALF_HEIGHT)
        self.paddles.append(new_paddle)
        self.screen.listen()
        self.screen.onkey(self.paddles[0].move_up, "w")
        self.screen.onkey(self.paddles[0].move_down, "s")
        self.screen.onkey(self.paddles[1].move_up, "Up")
        self.screen.onkey(self.paddles[1].move_down, "Down")
        self.ball = Ball()
        self.score_board = ScoreBoard()
        self.hit_count = 0
        self.game_running = True



    def run_loop(self):
        if self.game_running:
            if self.paddles[0].hit(self.ball):
                self.ball.reflect_horizontally()
                if self.hit_count % 10 == 0:
                    self.ball.increase_speed()
                self.hit_count += 1
                self.score_board.increment1()
            elif self.paddles[1].hit(self.ball):
                self.ball.reflect_horizontally()
                if self.hit_count % 10 == 0:
                    self.ball.increase_speed()
                self.hit_count += 1
                self.score_board.increment2()
            elif self.is_game_over():
                self.game_over_sequence()
            if self.ball.hit_horizontal_borders():
                self.ball.reflect_vertically()
            self.ball.move()
            self.screen.update()

    def is_game_over(self):
        ball_x_cor = self.ball.xcor()
        if ball_x_cor >= (SCREEN_HALF_WIDTH - BORDER - PADDLE_TURTLE_DIMENSION) or ball_x_cor <= (-SCREEN_HALF_WIDTH + BORDER + PADDLE_TURTLE_DIMENSION):
            return True
        else:
            return False

    def game_over_sequence(self):
        self.ball.stop()
        my_turtle = Turtle()
        my_turtle.color("white")
        my_turtle.hideturtle()
        my_turtle.penup()
        my_turtle.goto(x=int(-SCOREBOARD_WIDTH/2), y=0)
        message = "Game Over"
        my_turtle.write(arg=message, font=("Arial", 24, "bold"))
        self.game_running = False


pong = Pong()

is_game_running = True
while is_game_running:
    pong.run_loop()
    time.sleep(SLEEP_DURATION)


