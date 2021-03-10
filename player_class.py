from data.Memory.settings import *
import pygame
vec = pygame.math.Vector2

class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.player_start_pos = [pos.x, pos.y]
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.state = 'normal'
        # Min:0.1 Max:2.5 obs(so usar float)
        self.speed = self.set_speed()
        self.lives = 3
        self.itens = []

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        #configurando a posição na grid em referencia a posição em pixels
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER+
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER+
                            self.app.cell_height//2)//self.app.cell_height+1
        if self.on_coin():
            self.eat_coin()
            if self.current_score == self.app.maxcoin:
                print("entrou")
                self.app.state = 'win'

        if self.on_item():
            self.eat_item()
            if self.current_score == self.app.maxcoin:
                print("entrou")
                self.app.state = 'win'

    def draw_pac(self):
        image = pygame.image.load("data/images/PacMan2.png")
        image = pygame.transform.smoothscale(image, (int(self.app.cell_width),
                                                     int(self.app.cell_height)))
        self.app.screen.blit(image, (int(self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2,
                                     int(self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2))

    def draw(self):
        #self.draw_pac()
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR,
                          (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width//2-2)
        #desenhando as vidas do player
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (40+30*x, HEIGHT-15), 10)
        #pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                        self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2,
        #                                        self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        else:
            return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1
        if self.app.highscore < self.current_score:
            self.app.highscore += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        for gate in self.app.gates:
            if vec(self.grid_pos+self.direction) == gate:
                return False
        return True

    def set_speed(self):
        if self.state == 'awake':
            return 2
        else:
            return 1

    def on_item(self):
        if self.grid_pos in self.app.itens["pos"]:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        else:
            return False

    def eat_item(self):
        #na pos self.app.itens["pos"] tem um item
        for i in range(0, len(self.app.itens["pos"])):
            if self.grid_pos in self.app.itens["pos"]:
                if self.grid_pos == self.app.itens["pos"][i]:
                    if self.app.slot <= 4:
                        self.itens.append(self.app.itens["key"][i])
                        self.app.itens["pos"].pop(i)
                        self.app.itens["key"].pop(i)
                    else:
                        self.itens.pop()
                        self.itens.append(self.app.itens["key"][i])
                        self.app.itens["pos"].pop(i)
                        self.app.itens["key"].pop(i)
        self.current_score += 10
        if self.app.highscore < self.current_score:
            self.app.highscore += 10
