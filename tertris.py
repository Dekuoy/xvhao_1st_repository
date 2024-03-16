
"""
class
    screen   pixel   square  pool       

pixel 
    black red green yellow blue purple cyan white
"""

from collections.abc import Iterator
import sys
from enum import Enum
import time
import pygame
import random

BE  = "\033["
ESC = "\033[0m"
SPACE = "  "
BG_X = 2
BG_Y = 0
BG_WIDTH = 18
BG_HEIGHT = 30
SCREEN_W = 25
SCREEN_H = 30

class Color(Enum):
    
    BLACK   = BE + "40m" + SPACE + ESC
    RED     = BE + "41m" + SPACE + ESC
    GREEN   = BE + "42m" + SPACE + ESC
    YELLOW  = BE + "43m" + SPACE + ESC
    BLUE    = BE + "44m" + SPACE + ESC
    PURPLE  = BE + "45m" + SPACE + ESC
    CYAN    = BE + "46m" + SPACE + ESC
    WHITE   = BE + "47m" + SPACE + ESC

    
class Pixel:
    
    def __init__(self, color: str, x=0, y=0):
        self.color = color
        self._pixel = self.get_pixel()
        self.pixel = self._pixel
        self.pos = (x, y)
                
    def get_pixel(self):
        try :
            pixel = Color[self.color.upper()]
        except Exception as e:
            print("color %s not support" % self.color)
            sys.exit()  
        else:
            return pixel
    
    def __repr__(self):
        return f"pixel {self.color.lower()}"


class Screen:
    
    def __init__(self):
        self.width = 80
        self.height = 120
        self.buffer = None 

    def set_mode(self, width, height):
        self.width = width
        self.height = height
        
    def init(self):
        self.buffer = [[Color.BLACK.value for _ in range(self.width)] for _ in range(self.height)]
    
    def _buf_init(self):
            self.init()
    def update_pix(self, pix: str, pos: tuple[int, int]):
        try:
            x, y = pos 
            self.buffer[y][x] = pix
        except Exception as e:
            print("update pix fail")
            sys.exit()
        
    def display(self):
        buf = ""
        for row in self.buffer:
            for pix in row:
                buf += pix            
            buf += '\n'
        sys.stdout.write('\033[H\033[2J')   
        sys.stdout.flush() 
        sys.stdout.write(buf)
        self._buf_init()


class Background:
    
    def __init__(self):
        self.bg: list[Pixel]   = []
        self.goal = None
        self.text = None 
        self.x = BG_X
        self.y = BG_Y
        self.width = BG_WIDTH
        self.height = BG_HEIGHT
    
    def init(self):
        #      #
        #      #
        #      #
        ########
        for i in range(self.height - 1 ):
            self.bg.append(Pixel("blue", self.x , self.y + i))
            self.bg.append(Pixel("blue", self.x + self.width - 1, self.y + i))
        for j in range(self.width):
            self.bg.append(Pixel("blue", self.x +j, self.y + self.height - 1))
    
    
    def update(self, screen: Screen):

        for pix in self.bg:
            pos = pix.pos
            pix_value = pix.pixel.value
            screen.update_pix(pix_value, pos)



class SquareType(Enum):
    
    I = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
    O = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
        ]
    L = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
        ]
    J = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
        ]
    Z = [
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
        ]
    N = [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
        ]
    T = [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
        ]




class Square:
    ########
    ########
    ########
    ########
    TYPES = ["I", "O", "L", "J", "Z", "N", "T"]
    COLORS = ["white", "red", "green", "yellow", "purple", "cyan"]

    def __init__(self):
        self.x = (BG_X + BG_WIDTH) // 2
        self.y = 0
        self.pixels: list[list[Pixel]] = self._pixels()
        self.left = 0
        self.right = 0
        self._set_left()
        self._set_right()
        
    def _pixels(self):
        random.shuffle(Square.COLORS)
        random.shuffle(Square.TYPES)
        color = Square.COLORS[0]
        tp = SquareType[Square.TYPES[0]].value
        # tp = SquareType.L.value
        pixels = [[None for _ in range(4)] for _ in range(4)]
        # print(pixels)
        if len(tp )!= 4:
            print(tp)
            assert(len(tp) == 4)
        for i in range(4):
            for j in range(4):
                if len(tp[i]) != 4:
                    print(tp)
                    assert(len(tp[i] == 4))
                if tp[i][j]:
                    pixels[i][j] = Pixel(color)
        return pixels
    
    def _set_left(self):
        
        for i in range(4):
            for j in range(4):
                if self.pixels[j][i]  != None:
                    self.left = i
                    return True
        assert(0)

    def _set_right(self):
        for i in range(3, -1, -1):
            for j in range(4):
                if self.pixels[j][i] != None:
                    self.right = i
                    return True
        assert(0)        
        
    
    def move(self, direction: str):
        is_sus = False 
        match direction:
            case "down":
                self.y += 1
                is_sus = True
            case "up":
                self.y -= 1
                is_sus = True
            case "left":
                if self.x - 1 + self.left > BG_X:
                    self.x -= 1
                    is_sus = True
                else:
                    is_sus = False
            case "right":
                if self.x + 1 + self.right < BG_X + BG_WIDTH - 1:
                    self.x += 1
                    is_sus = True
                else:
                    is_sus = False
            case _:
                assert(0)
        self._update_pos()
        return is_sus

    def rotate(self, direction="left"):
        ########  right (x, y) -> F(x, y) -> (3 - y, x)
    #   --------  left  (x, y) -> F(x, y) -> (y, 3 - x)
        ########
        ########   
        pix = [[None for _ in range(4)] for _ in range(4)]
        match direction:
            
            case "left":
                for x in range(4):
                    for y in range(4):
                        pix[y][x] = self.pixels[3 - x][y]
            case "right":
                for x in range(4):
                    for y in range(4):
                        pix[y][x] = self.pixels[x][3 - y]
            case _:
                assert(0)
        self.pixels = pix
        self._update_pos()
        self._set_left()
        self._set_right()
    
    def is_top(self) -> bool:
        return self.y == 0
    def _update_pos(self):
        for i in range(4):
            for j in range(4):
                if self.pixels[i][j]:
                    self.pixels[i][j].pos = (self.x + j, self.y + i)
    def update(self, screen: Screen):
        self._update_pos()
        for i in range(4):
            for j in range(4):
                pix = self.pixels[i][j]
                if pix:
                    screen.update_pix(pix.pixel.value, pix.pos)

    def __iter__(self) -> Iterator[Pixel]:
        for i in range(4):
            for j in range(4):
                if self.pixels[i][j]:
                    yield self.pixels[i][j]
                


class Pool:
    
    def __init__(self):
        self.width = BG_WIDTH - 2
        self.height = BG_HEIGHT - 1
        self.buffer: list[list[str]] = self.init_buffer()

    def add(self, square: Square):
        
        for pix in square:
            x, y = self._screen_pos_to_pool(pix.pos)
            self.buffer[y][x] = pix.pixel.value
    
    def _screen_pos_to_pool(self, pos: tuple[int, int]):
        x, y = pos
        return x - BG_X - 1, y
    
    def _pool_pos_to_screen(self, pos: tuple[int,int]):
        x, y = pos
        return x + BG_X + 1, y
        
    def init_buffer(self):
        buf = [[None for _ in range(self.width)] for _ in range(self.height)]

        return buf


    def update(self, screen: Screen):
        for i in range(self.height):
            for j in range(self.width):
                pix = self.buffer[i][j]
                if pix:
                    x, y = self._pool_pos_to_screen((j, i))
                    screen.update_pix(pix, (x, y))
    
    def _check_full(self, row: int):
        full = True
        for pix in self.buffer[row]:
            if not pix:
                full = False
                break
        return full
            
    def is_in_pool(self, pos: tuple[int, int]) -> bool:
        x, y = self._screen_pos_to_pool(pos)
        if self.buffer[y][x]:
            return True
        else:
            return False
        
        
    def check_lines(self) -> list[int]:
        full_rows = []
        for row in range(len(self.buffer)):
            full = self._check_full(row)
            if full:
                full_rows.append(row)
        return full_rows
    
    def rank(self, full_rows: list[int]):
        all_rows = [x for x in range(self.height)]
        for row in full_rows:
            all_rows.remove(row)
        all_rows.sort(reverse=True)
        new_rows = [[None for _ in range(self.width)] for _ in range(self.height)]
        for i in range(len(all_rows)):
            new_rows[self.height - i - 1]  = self.buffer[all_rows[i]]
        
        self.buffer = new_rows  
            
    

class Event:
    
    QUIT    = pygame.QUIT
    K_UP    = pygame.K_UP
    K_DOWN  = pygame.K_DOWN
    K_LEFT  = pygame.K_LEFT
    K_RIGHT = pygame.K_RIGHT
    K_q     = pygame.K_q
    KEYDOWN = pygame.KEYDOWN
    KEYUP   = pygame.KEYUP
    
    def __init__(self):
        pass
    def init(self):
        pygame.init()
        pygame.display.set_mode((1, 1), flags=pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.event = pygame.event
    
    def get(self):
        return self.event.get()

    def close(self):
        pygame.quit()
    

def check_crash(pool: Pool, square: Square):
    
    for pix in square:
        x, y  = pix.pos
        if y >= pool.height:
            return True
        if pool.is_in_pool((x, y)):
            return True
        
    return False
    


def main():
    screen = Screen()
    # screen_width, screen_height
    screen.set_mode(SCREEN_W, SCREEN_H)
    screen.init()
    bg = Background()
    bg.init()
   
    cur_square = None
    running = True
    events = Event()
    events.init()
    pool = Pool()
       
    while running:
        
        if not cur_square:
            cur_square = Square()
            # cur_square.move("up")
        
        for event in events.get():
            if event.type == Event.QUIT: 
                running = False
                break
            elif event.type == Event.KEYDOWN:
                match event.key:
                    case Event.K_q:
                        running = False
                        break
                    case Event.K_LEFT:
                        if cur_square.move("left"):
                            if check_crash(pool, cur_square):
                                cur_square.move("right")
                    case Event.K_RIGHT:
                        if cur_square.move("right"):
                            if check_crash(pool, cur_square):
                                cur_square.move("left")
                    case Event.K_DOWN:
                        while True:
                            cur_square.move("down")
                            if check_crash(pool, cur_square):
                                cur_square.move("up")
                                break
                    case Event.K_UP:
                        cur_square.rotate("right")
                        if check_crash(pool, cur_square):
                            cur_square.rotate("left")
                    case _:
                        pass

        if not running:
            continue        
        
        time.sleep(.1)
        
        cur_square.move("down")
        if check_crash(pool, cur_square):
            cur_square.move("up")
            pool.add(cur_square)
            cur_square = None
        else:
            cur_square.update(screen)
        
        full_rows = pool.check_lines()
        if len(full_rows) != 0:
            pool.rank(full_rows)
            
        pool.update(screen)
        
        events.clock.tick(30)
        bg.update(screen)
        screen.display()
        time.sleep(0.2)
    
    events.close()


if __name__ == "__main__":
    main()
    