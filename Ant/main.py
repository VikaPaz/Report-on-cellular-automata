import pygame as pg
import sys
import tkinter as tk
from tkinter import colorchooser

anthill = [[0 for _ in range(100)] for _ in range(100)]
antmovement = [[0 for _ in range(100)] for _ in range(100)]
color = [(255, 255, 255)]


class Field:
    def stand_ant(self, screen, mouse_pos):
        pg.draw.rect(screen, (255, 0, 0),
                     ((mouse_pos[0] - (mouse_pos[0] % 5), mouse_pos[1] - (mouse_pos[1] % 5)), (5, 5)))
        antmovement[mouse_pos[0] // 5][mouse_pos[1] // 5] = 2


class Ant(Field):
    def __init__(self):
        self.x, self.y = self.check()
        self.rotation = 0
        self.color_number = anthill[self.x][self.y]

    def check(self):
        for y, i in enumerate(antmovement):
            if 2 in i:
                x = i.index(2)
                return int(y), int(x)

    def rotate(self):
        if self.color_number == 0 or self.color_number == 5:
            self.rotation += 1
            anthill[self.x][self.y] = 1
        if self.color_number == 1:
            self.rotation -= 1
            anthill[self.x][self.y] = 5
        self.rotation = self.rotation % 4

    def move(self):
        if self.rotation == 0:
            error = (self.y - 1) % 100
            antmovement[self.x][error] = 2
            self.y = error
        elif self.rotation == 1:
            error = (self.x + 1) % 100
            antmovement[error][self.y] = 2
            self.x = error
        elif self.rotation == 2:
            error = (self.y + 1) % 100
            antmovement[self.x][error] = 2
            self.y = error
        elif self.rotation == 3:
            error = (self.x - 1) % 100
            antmovement[error][self.y] = 2
            self.x = error

        antmovement[self.x][self.y] = 0
        self.color_number = anthill[self.x][self.y]
        # print(self.x, self.y, self.rotation, self.color_number, anthill[self.x][self.y])

    def draw(self, screen):
        global color
        for i in range(0, 500, 5):
            for j in range(0, 500, 5):
                if anthill[i // 5][j // 5] == 1:
                    pg.draw.rect(screen, color[0],
                                 ((i, j), (5, 5)))
                elif anthill[i // 5][j // 5] == 0:
                    pg.draw.rect(screen, (0, 0, 0),
                                 ((i, j), (5, 5)))
                else:
                    r, g, b = color[0]
                    pg.draw.rect(screen, (255 - r, 255 - g, 255 - b),
                                 ((i, j), (5, 5)))
        pg.draw.rect(screen, (255, 255, 255),
                     ((int(self.x * 5), int(self.y * 5)), (5, 5)))


def palette():
    global color
    color = tk.colorchooser.askcolor()
    window.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    button = tk.Button(text='color', height=5, width=10, background='#000000', command=palette, foreground='#ffffff')
    button.pack()
    window.mainloop()

    pg.init()
    screen = pg.display.set_mode((500, 500))
    clock = pg.time.Clock()
    screen.fill((0, 0, 0))
    field = Field()
    button = pg.Rect(100, 100, 50, 50)

    flag = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # sys.exit()
                pg.quit()
                flag = False
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                field.stand_ant(screen, event.pos)
                ant = Ant()
                flag = True
        if flag:
            ant.rotate()
            ant.move()
            ant.draw(screen)
            pg.display.flip()
            clock.tick(60)
        else:
            pass
            # break