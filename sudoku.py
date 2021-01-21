import pygame
import random
pygame.init()

class Grid:
    boards = [
    [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ],[
        [0, 0, 7, 0, 0, 2, 9, 3, 0],
        [0, 8, 1, 0, 0, 0, 0, 0, 5],
        [9, 0, 4, 7, 0, 0, 1, 6, 0],
        [0, 1, 0, 8, 0, 0, 0, 0, 6],
        [8, 4, 6, 0, 0, 0, 5, 9, 2],
        [5, 0, 0, 0, 0, 6, 0, 1, 0],
        [0, 9, 2, 0, 0, 8, 3, 0, 1],
        [4, 0, 0, 0, 0, 0, 6, 5, 0],
        [0, 6, 5, 4, 0, 0, 2, 0, 0]
    ],[
        [0, 6, 0, 3, 0, 0, 8, 0, 4],
        [5, 3, 7, 0, 9, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 6, 3, 0, 7],
        [0, 9, 0, 0, 5, 1, 2, 3, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 1, 3, 6, 2, 0, 0, 4, 0],
        [3, 0, 6, 4, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 6, 0, 5, 2, 3],
        [1, 0, 2, 0, 0, 9, 0, 8, 0]
    ],
    ]
    board = boards[random.randint(0,2)]

    def __init__(self, r, c, width, height, window):
        self.r = r
        self.c = c
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(c)] for i in range(r)]
        self.width = width
        self.height = height
        self.model = None
        self.updateModel()
        self.selected = None
        self.window = window

    def updateModel(self):
        self.model = [[self.cubes[i][j].value for j in range(self.c)] for i in range(self.r)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.updateModel()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.updateModel()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        gap = self.width / 9
        for i in range(self.r+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.r):
            for j in range(self.c):
                self.cubes[i][j].draw(self.window)

    def select(self, row, col):
        for i in range(self.r):
            for j in range(self.c):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def isFinished(self):
        for i in range(self.r):
            for j in range(self.c):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                if self.solve():
                    return True
                self.model[row][col] = 0

        return False

    def solvingGUI(self):
        self.updateModel()
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].drawChange(self.window, True)
                self.updateModel()
                pygame.display.update()
                pygame.time.delay(100)
                if self.solvingGUI():
                    return True
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.updateModel()
                self.cubes[row][col].drawChange(self.window, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False


class Cube:
    r = 9
    c = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (0,0,110))
            window.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0,0,0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (0,0,255), (x,y, gap ,gap), 3)

    def drawChange(self, window, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(window, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(window, (0, 255, 0), (x, y, gap, gap), 2)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 2)


    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def findEmpty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None


def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def redrawWindow(window, board, cross):
    fnt = pygame.font.SysFont("comicsans", 30)
    window.fill((173, 216, 230))
    text = fnt.render("X " * cross, 1, (0, 0, 0))
    window.blit(text, (20, 560))
    board.draw()

def main():
    print('\nThe classic Sudoku game involves a grid of 81 squares. \nThe grid is divided into nine blocks, each containing nine squares.\nThe rules of the game are simple: each of the nine blocks \nhas to contain all the numbers 1-9 within its squares. \nEach number can only appear once in a row, column or box.')
    print('\nInstructions: \n1.Click to select a cube.\n2.You can sketch down your number. And use Enter to submit it.\n(Crosses are shown for wrong answers)\n3.Use space bar to show the solution\n')
    window = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Game")
    board = Grid(9, 9, 540, 540, window)
    key = None
    executing = True
    cross = 0
    while executing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solvingGUI()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Right Choice")
                        else:
                            print("Wrong Choice")
                            cross += 1
                        key = None
                        if board.isFinished():
                            print("Game closed")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redrawWindow(window, board, cross)
        pygame.display.update()

main()
pygame.quit()
