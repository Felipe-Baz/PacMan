import json
import sys
from enemy_class import *
from player_class import *

# Inicializa o pygame
pygame.init()
# Cria um vector2 denominado vec
vec = pygame.math.Vector2

# Define uma classe App
class App:
    def __init__(self):
        # Cria a tela, usando o pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # Cria o clock, usando o pygame
        self.clock = pygame.time.Clock()
        # Configura o estado inicial do running do App como "rodando" ,ou seja, True.
        self.running = True
        # Configura o estado do app como "Start", ou seja, "iniciando".
        self.background = None
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.player_pos = None
        self.enemies = []
        self.enemy_pos = []
        # pos of slots
        self.backpack = []
        self.slot = 0
        self.itens = {"pos": [], "key": []}
        self.itens_images = []
        self.gates = []
        self.highscore = 0
        self.maxcoin = 0
        self.load()
        print(self.maxcoin)
        self.player = Player(self, vec(self.player_pos))
        self.make_enemies()

    # Cria o metodo run, cujo será o metodo de inicialização do jogo.
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'win':
                self.game_win_events()
                self.game_win_update()
                self.game_win_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

########################### HELP FUNCTIONS ###############################

    # função para escrita na tela, com as configurações corretas.
    @staticmethod
    def draw_text(words, screen, pos,
                  size, colour, font_name, center=True):
        # Seleciona a fonte
        font = pygame.font.SysFont(font_name, size)
        # Seleciona o texto, já aplicando a cor
        text = font.render(words, False, colour)
        # Armazena o valor do tamanho da frase
        text_size = text.get_size()
        # Faz os ajustes caso seja necessario, para que a frase fique centro.
        if center:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2

        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('data/images/maze.png')
        self.background = pygame.transform.scale(self.background,
                                                 (MAZE_WIDTH, MAZE_HEIGHT))
        self.itens_images.append(pygame.image.load('data/itens/cruz.png'))
        self.itens_images.append(pygame.image.load('data/itens/garfo.png'))
        self.itens_images.append(pygame.image.load('data/itens/granada.png'))
        self.itens_images.append(pygame.image.load('data/itens/mascara.png'))
        self.itens_images.append(pygame.image.load('data/itens/raio.png'))
        self.high_score()

        # abrindo o arquivo do mapa

        with open("data/Memory/walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        # criando a lista das paredes, com as coordenadas delas
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        # criando a lista dos moedas, com as coordenadas delas
                        self.coins.append(vec(xidx, yidx))
                        self.maxcoin += 1
                    elif char == "P":
                        # encontra a posição de inicio do player
                        self.player_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        # encontra a posição de inicio dos mobs
                        self.enemy_pos.append([xidx, yidx])
                    elif char == "B":
                        # criando a lista das portas, com as coordenadas delas
                        pygame.draw.rect(self.background, BACKGROUND, (xidx * self.cell_width, yidx * self.cell_height,
                                                                       self.cell_width, self.cell_height))
                        self.gates.append(vec(xidx, yidx))
                    elif char == "W":  # item 1 "Weapon"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(1)
                        self.maxcoin += 10
                    elif char == "H":  # item 2 "Hungry"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(2)
                        self.maxcoin += 10
                    elif char == "D":  # item 3 "Drunk"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(3)
                        self.maxcoin += 10
                    elif char == "S":  # item 4 "Scared"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(4)
                        self.maxcoin += 10
                    elif char == "R":  # item 5 "Awake"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(5)
                        self.maxcoin += 10

    def make_enemies(self):
        for idx, pos in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, COIN_COLOUR, (int(coin.x * self.cell_width) + self.cell_width // 2
                                                          + TOP_BOTTOM_BUFFER // 2, int(coin.y * self.cell_height) +
                                                          self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def draw_itens(self):
        for i, item in enumerate(self.itens["pos"]):
            number = self.itens["key"][i]
            image = pygame.transform.smoothscale(self.itens_images[number - 1], (int(self.cell_width),
                                                                                 int(self.cell_height)))
            self.screen.blit(image, (int(item.x * self.cell_width)+ TOP_BOTTOM_BUFFER//2,
                                     int(item.y*self.cell_height)+TOP_BOTTOM_BUFFER//2))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.player_start_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        self.player.itens *= 0

        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.enemy_start_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("data/Memory/walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "W":  # item 1 "Weapon"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(1)
                    elif char == "H":  # item 2 "Hungry"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(2)
                    elif char == "D":  # item 3 "Drunk"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(3)
                    elif char == "S":  # item 4 "Scared"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(4)
                    elif char == "R":  # item 5 "Awake"
                        self.itens["pos"].append(vec(xidx, yidx))
                        self.itens["key"].append(5)
        self.state = 'playing'

    def draw_backpack(self):
        self.draw_text('LIVES', self.screen, [140 // 2, HEIGHT - (FOOTER + 30) // 2], 20, ORANGE_START_MENU, START_FONT)
        # faz o quadrado de slot
        for x in range(0, 4):
            xidx = 190 + x * (SLOT_WIDTH + SPACING) + 2
            yidx = MAZE_HEIGHT + TOP_BOTTOM_BUFFER // 2 + 42
            pygame.draw.rect(self.screen, RED,
                             (190 + x * (SLOT_WIDTH + SPACING), MAZE_HEIGHT + TOP_BOTTOM_BUFFER // 2 + 40,
                              SLOT_WIDTH, SLOT_HEIGHT))
            pygame.draw.rect(self.screen, BACKGROUND, (xidx, yidx, SLOT_WIDTH - 4, SLOT_HEIGHT - 4))
            self.backpack.append(vec(xidx, yidx))

    def draw_itens_backpack(self):
        for slot, item in enumerate(self.player.itens):
            image_edit = pygame.transform.smoothscale(self.itens_images[item-1], (int(SLOT_WIDTH - 2),
                                                                                      int(SLOT_HEIGHT - 2)))
            self.screen.blit(image_edit, (self.backpack[slot].x, self.backpack[slot].y))
            #self.screen.blit(image, (int(item.x * self.cell_width) + TOP_BOTTOM_BUFFER // 2,
            #                         int(item.y * self.cell_height) + TOP_BOTTOM_BUFFER // 2))
        self.slot = len(self.player.itens)+1

    def high_score(self):
        with open(f'data/Memory/HighScore.json') as fp:
            high = json.load(fp)
        self.highscore = high["HighScore"]
        fp.close()

########################## Start FUNCTIONS ###############################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # caso os eventos acabem, sera o running como "False", ou seja, o jogo foi encerrado.
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Configura o estado como "Jogando"
                self.state = 'playing'

    def start_update(self):
        pass

    # Metodo de escrita na tela
    def start_draw(self):
        # Pinta o fundo da cor de background
        self.screen.fill(BACKGROUND)
        # Faz a escrita na tela
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH // 2, HEIGHT // 2 - 50],
                       START_TEXT_SIZE, ORANGE_START_MENU, START_FONT)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH // 2, HEIGHT // 2],
                       START_TEXT_SIZE, CYAN_START_MENU, START_FONT)
        self.draw_text(f'HIGH SCORE: {self.highscore}', self.screen, [3, 0],
                       START_TEXT_SIZE, WHITE_START_MENU, START_FONT, center=False)
        self.draw_text('Credits: FelipeBazCode', self.screen, [5, HEIGHT - 25],
                       START_TEXT_SIZE, GREEN_START_MENU, START_FONT, center=False)
        # Atualiza a screen, aplicando o texto de inicio
        pygame.display.set_caption("PacMan - By FelipeBazCode")
        icon = pygame.image.load("data/images/pacman.png").convert_alpha()
        w, h = icon.get_size()
        image = pygame.transform.smoothscale(icon, (int(w*0.25), int(h*0.25)))
        pygame.display.set_icon(icon)
        self.screen.blit(image, ((WIDTH+(w*0.25))//4, HEIGHT//4-150))
        pygame.display.update()

########################## Playing FUNCTIONS ###############################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # caso os eventos acabem, sera o running como "False", ou seja, o jogo foi encerrado.
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(vec(0, 1))
                # Pause
                if event.key == pygame.K_ESCAPE:
                    self.pause_game()

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.die()

    # Metodo de escrita na tela
    def playing_draw(self):
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        # self.draw_grid()
        self.draw_coins()
        self.draw_text(f'SCORE: {self.player.current_score}', self.screen, [26, 2],
                       START_TEXT_SIZE, GREEN_START_MENU, START_FONT, center=False)
        self.draw_text(f'HIGH SCORE: {self.highscore}', self.screen, [WIDTH // 2 + 70, 13],
                       START_TEXT_SIZE, GREEN_START_MENU, START_FONT)
        self.draw_backpack()
        self.draw_itens()
        self.draw_itens_backpack()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def die(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            atual_score = {"HighScore": self.player.current_score}
            # salva as informações do dicionario de informações relevantes em um arquivo .json para analise
            with open(f'data/Memory/HighScore.json', 'w') as json_file:
                json.dump(atual_score, json_file, indent=3, ensure_ascii=False)
            json_file.close()
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.player_start_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.enemy_start_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def pause_draw(self):
        # Pinta o fundo da cor de background
        self.screen.fill(BACKGROUND)
        # Faz a escrita na tela
        self.draw_text('To resume press ENTER or ESCAPE', self.screen, [WIDTH // 2, HEIGHT // 2 - 50],
                       START_TEXT_SIZE, ORANGE_START_MENU, START_FONT)
        self.draw_text('To QUIT Press Q', self.screen, [WIDTH // 2, HEIGHT // 2],
                       START_TEXT_SIZE, CYAN_START_MENU, START_FONT)
        self.draw_text(f'Current Score: {self.player.current_score}', self.screen, [3, 0],
                       START_TEXT_SIZE, WHITE_START_MENU, START_FONT, center=False)
        self.draw_text('Credits: FelipeBazCode', self.screen, [5, HEIGHT - 25],
                       START_TEXT_SIZE, GREEN_START_MENU, START_FONT, center=False)
        icon = pygame.image.load("data/images/pacman.png").convert_alpha()
        w, h = icon.get_size()
        image = pygame.transform.smoothscale(icon, (int(w * 0.25), int(h * 0.25)))
        self.screen.blit(image, ((WIDTH + (w * 0.25)) // 4, HEIGHT // 4 - 150))
        pygame.display.update()

    def pause_game(self):
        self.pause_draw()
        cond_quit = True
        while cond_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # caso os eventos acabem, sera o running como "False", ou seja, o jogo foi encerrado.
                    self.running = False
                    cond_quit = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        cond_quit = False
                    if event.key == pygame.K_q:
                        self.running = False
                        cond_quit = False

########################## Game Over FUNCTIONS ###############################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # caso os eventos acabem, sera o running como "False", ou seja, o jogo foi encerrado.
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Configura o estado como "Jogando"
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BACKGROUND)
        quit_text = "Press Escape to QUIT"
        again_text = "Press Space bar to Play again"
        self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100],
                       GAME_OVER_TEXT_SIZE, RED, START_FONT)
        self.draw_text(again_text, self.screen, [WIDTH // 2, HEIGHT // 2],
                       GAME_OVER_TEXT_SIZE - 10, GREY, START_FONT)
        self.draw_text(quit_text, self.screen, [WIDTH // 2, HEIGHT // 2 + 50],
                       GAME_OVER_TEXT_SIZE - 10, RED, START_FONT)
        pygame.display.update()

########################## Game Over FUNCTIONS ###############################

    def game_win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # caso os eventos acabem, sera o running como "False", ou seja, o jogo foi encerrado.
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Configura o estado como "Jogando"
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_win_update(self):
        pass

    def game_win_draw(self):
        self.screen.fill(BACKGROUND)
        quit_text = "Press Escape to QUIT"
        again_text = "Press Space bar to Play again"
        self.draw_text("YOU WON!!", self.screen, [WIDTH//2, (HEIGHT//2)-50],
                       GAME_OVER_TEXT_SIZE, RED, START_FONT)
        self.draw_text(again_text, self.screen, [WIDTH//2, HEIGHT//2],
                       GAME_OVER_TEXT_SIZE-10, GREY, START_FONT)
        self.draw_text(quit_text, self.screen, [WIDTH//2, HEIGHT//2+50],
                       GAME_OVER_TEXT_SIZE-10, RED, START_FONT)
        trofeu = pygame.image.load("data/images/trofeu.png").convert_alpha()
        w, h = trofeu.get_size()
        image = pygame.transform.smoothscale(trofeu, (int(w*0.10), int(h*0.10)))
        self.screen.blit(image, ((WIDTH-15)//3, HEIGHT//4-150))
        pygame.display.update()
