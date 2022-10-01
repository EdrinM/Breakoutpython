from tkinter import Tk, Canvas
from winsound import *

root = Tk()
root.title('Breakout :)')

WIDTH, HEIGHT = 600, 600

GREEN = 'green'
YELLOW = 'yellow'
RED = 'red'

BRICKS = [GREEN, YELLOW, RED]

SIZE = 10

game_running = True


class Brick:
    def __init__(self, row, col, type=GREEN):
        self.type = type
        self.row = row
        self.col = col
        self.width = int(WIDTH/SIZE)
        self.height = int(HEIGHT/(SIZE*2.5))
        self.startx = 0
        self.starty = HEIGHT*0.1
        self.x = self.startx + self.width*self.col
        self.y = self.starty + self.height*self.row
        self.hits = 0
        if self.type == GREEN:
            self.hits = 0
        elif self.type == YELLOW:
            self.hits = 1
        elif self.type == RED:
            self.hits = 2

    def change_brick(self):
        self.hits -= 1
        self.type = BRICKS[self.hits]

    def check_collision(self, ball):
        future_ball_x = ball.x+ball.speed_x
        future_ball_y = ball.y+ball.speed_y
        if self.y <= future_ball_y < self.y+self.height:
            if ((future_ball_x+ball.radius) > self.x and future_ball_x < self.x or
                (future_ball_x-ball.radius) < self.x+self.width and future_ball_x > self.x+self.width):
                ball.deflect(-1, 1)
                PlaySound('hit.wav', SND_ASYNC)
                if self.hits == 0:
                    return True
                else:
                    self.change_brick()

        if self.x <= future_ball_x < self.x+self.width:
            if (((ball.y+ball.radius) > self.y and future_ball_y < self.y) or 
                ((ball.y-ball.radius) < self.y+self.height and ball.y > self.y+self.height)):
                ball.deflect(1, -1)
                PlaySound('hit.wav', SND_ASYNC)
                if self.hits == 0:
                    return True
                else:
                    self.change_brick()
        return False

    def draw(self, canvas):
        
        x1 = self.x+self.width
        y1 = self.y+self.height
        canvas.create_rectangle(
            self.x, self.y, x1, y1, fill=self.type, outline='white')


class Grid:
    def __init__(self, level) -> None:
        self.level = level
        self.grid = self.get_grid()
        self.bricks_count = SIZE*SIZE

    def get_grid(self):
        grid = []
        if self.level == 1:
            for i in range(SIZE):
                if i % 2 == 0:
                    continue
                row = []
                for j in range(SIZE):
                    row.append(Brick(i, j))
                grid.append(row)

            return grid

        if self.level == 2:
            for i in range(SIZE):
                if i % 2 == 0:
                    continue
                row = []
                for j in range(SIZE):
                    if j % 2 == 0:
                        row.append(Brick(i, j))
                    else:
                        row.append(Brick(i, j, YELLOW))
                grid.append(row)

            return grid

        if self.level == 3:
            for i in range(SIZE):
                row = []
                for j in range(SIZE):
                    if i % 2 == 0:
                        row.append(Brick(i, j, BRICKS[(j % 3)]))
                    else:
                        row.append(Brick(i, j))
                grid.append(row)

            return grid

        if self.level == 4:
            for i in range(SIZE):
                row = []
                for j in range(SIZE):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            row.append(Brick(i, j))
                        else:
                            row.append(Brick(i, j, YELLOW))
                    else:
                        if j % 2 == 0:
                            row.append(Brick(i, j))
                        else:
                            row.append(Brick(i, j, RED))
                grid.append(row)

            return grid

        if self.level == 5:
            for i in range(SIZE):
                row = []
                for j in range(SIZE):
                    row.append(Brick(i, j, BRICKS[i % 3]))
                grid.append(row)

            return grid

    def check_collision(self, ball):
        self.bricks_count = 0
        new_grid = []
        for row in self.grid:
            new_row = []
            for brick in row:
                if not brick.check_collision(ball):
                    self.bricks_count += 1
                    new_row.append(brick)
            new_grid.append(new_row)
        self.grid = new_grid

    def get_brick_count(self):
        return self.bricks_count

    def next_grid(self):
        if self.level > 4:
            return
        PlaySound('advancement.wav', SND_ASYNC)
        self.level += 1
        self.grid = self.get_grid()

    def draw(self, canvas):
        for row in self.grid:
            for brick in row:
                brick.draw(canvas)


class Ball:
    def __init__(self) -> None:
        self.radius = 10
        self.reset()
        self.lives = 3

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x-self.radius < 0 or self.x+self.radius > WIDTH:
            self.deflect(-1, 1)
        if self.y-self.radius < 0 or self.y+self.radius > HEIGHT:
            self.deflect(1, -1)

    def deflect(self, speed_x, speed_y):
        self.speed_x *= (speed_x)
        self.speed_y *= (speed_y)

    def reset(self):
        self.x = WIDTH*0.5
        self.y = HEIGHT*0.9
        self.speed_x, self.speed_y = 6, -4

    def decrease_lives(self):
        if self.lives < 1:
            return
        PlaySound('loselife.wav', SND_ASYNC)
        self.lives -= 1
        self.reset()

    def draw(self, canvas):
        self.move()
        x0 = self.x - self.radius
        y0 = self.y - self.radius
        x1 = self.x + self.radius
        y1 = self.y + self.radius
        canvas.create_oval(x0, y0, x1, y1, fill='white', outline='white')


class Paddle:
    def __init__(self) -> None:
        self.height = 5
        self.width = WIDTH*0.2

        self.x = WIDTH*0.5
        self.y = HEIGHT*0.95

        self.speed = 10

        self.dir = 1

        self.moving = False

    def move(self):

        if not self.moving:
            return

        self.x += self.speed*self.dir

        if self.x < 0 or self.x+self.width > WIDTH:
            self.x -= self.speed*self.dir

    def set_speed(self, x):
        self.moving = True
        self.dir = x

    def stop(self):
        self.moving = False

    def check_ball_collision(self, ball):
        global game_running
        if ball.y+ball.radius >= self.y:
            if self.x <= (ball.x - ball.radius) <= (ball.x + ball.radius)  <= self.x+self.width:
                PlaySound('pad.wav', SND_ASYNC)
                ball.deflect(1, -1)
            else:
                ball.decrease_lives()
                if ball.lives <= 0:
                    game_running = False

    def draw(self, canvas):
        x0 = self.x
        y0 = self.y

        x1 = x0+self.width
        y1 = y0+self.height

        canvas.create_rectangle(
            x0, y0, x1, y1, fill='white', outline='white')


class Game(Canvas):
    def __init__(self, master):
        self.level = 1
        self.game_won = False
        super().__init__(master, bg='black', width=WIDTH, height=HEIGHT)
        self.pack()

        self.grid = Grid(self.level)
        self.grid.draw(self)

        self.ball = Ball()
        self.ball.draw(self)

        self.paddle = Paddle()
        self.paddle.draw(self)

        self.key_pressed = None

        master.bind('<KeyPress>', self.move_paddle)
        master.bind('<KeyRelease>', self.stop_paddle)

        self.game_loop()

    def move_paddle(self, e):
        
        if e.keysym == 'Left' and self.key_pressed == None:
            self.key_pressed = 1
            self.paddle.set_speed(-1)
        elif e.keysym == 'Right' and self.key_pressed == None:
            self.key_pressed = 1
            self.paddle.set_speed(1)

    def stop_paddle(self, e):
        if e.keysym == 'Left' or e.keysym == 'Right':
            self.key_pressed = None
            self.paddle.stop()

    def next_level(self):
        global game_running
        self.level += 1
        self.ball.reset()
        self.grid.next_grid()
        if self.level >= 6:
            self.game_won = True
            game_running = False

    def check_bricks_count(self):
        if self.grid.get_brick_count() == 0:
            self.next_level()

    def show_lives(self):
        x = WIDTH*0.9
        y = HEIGHT*0.05
        self.create_text(
            x, y, text=f'lives left:{self.ball.lives}', font=('Ariel', 16, 'normal'), fill='white')

    def show_level(self):
        x = WIDTH/2
        y = HEIGHT*0.05
        self.create_text(
            x, y, text=f'Level:{self.level}', font=('Ariel', 29, 'normal'), fill='white')

    def show_message(self, text):
        x = WIDTH*0.5
        y = HEIGHT*0.5
        self.create_text(
            x, y, text=text, font=('Ariel', 35, 'normal'), fill='white')

    def game_loop(self):
        self.delete('all')
        self.show_lives()
        self.show_level()
        self.check_bricks_count()
        self.ball.draw(self)
        self.paddle.move()
        self.paddle.draw(self)
        self.paddle.check_ball_collision(self.ball)
        self.grid.check_collision(self.ball)
        self.grid.draw(self)
        if game_running:
            root.after(ms=10, func=self.game_loop)
        if self.game_won:
            self.show_message('Game won!!!')
        if self.ball.lives <= 0:
            self.show_message('Game Lost!!')


if __name__ == '__main__':
    g = Game(root)


root.mainloop()
