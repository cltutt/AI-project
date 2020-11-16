import pygame
import neat
import math
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

CONFIG_FILE = 'config-feedforward.txt'

screen = pygame.display.set_mode([1500, 1000])
pygame.display.set_caption('Maze Runner')


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x

    def get_x(self):
        return self.rect.x

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color, speed_x, speed_y):

      super().__init__()
      self.image = pygame.Surface([width, height])
      self.image.fill(color)

      self.rect = self.image.get_rect()
      self.rect.y = y 
      self.rect.x = x 

      self.speed_x = speed_x
      self.speed_y = speed_y

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def enemymove(self, walls, dt):
        self.rect.x += self.speed_x * dt

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.speed_x > 0:
                self.rect.right = block.rect.left
                self.speed_x = -self.speed_x
            else:
                self.rect.left = block.rect.right
                self.speed_x = -self.speed_x

        self.rect.y += self.speed_y * dt

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
                self.speed_y = -self.speed_y
            else:
                self.rect.top = block.rect.bottom
                self.speed_y = -self.speed_y

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.deaths = 0

        self.change_x = 10
        self.change_y = 10

    def num_deaths(self):
        return self.deaths

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_closest_wall(self, walls):
        wall_list = walls
        min = -1000
        distance = 0
        for wall in wall_list:
            distace = self.rect.x - wall.get_x()
            if distance < min:
                min = distance
            return abs(distance)

    def get_closest_enemy(self, enemies):
        enemy_list = enemies
        min = -1000
        distance = 0
        for enemy in enemy_list:
            distace = self.rect.x - enemy.get_x()
            if distance < min:
                min = distance
        return abs(distance)

    def collide_with_enemy(self, enemies):
        return pygame.sprite.spritecollide(self, enemies, False)

    def move_right(self, walls, enemies, starting_x, starting_y):

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left

        if self.collide_with_enemy(enemies):
          self.rect.x = starting_x
          self.rect.y = starting_y

    def move_left(self, walls, enemies, starting_x, starting_y):

        self.rect.x -= self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:
            if self.change_x < 0:
                self.rect.left = block.rect.right

        if self.collide_with_enemy(enemies):
            self.rect.x = starting_x
            self.rect.y = starting_y

    def move_up(self, walls, enemies, starting_x, starting_y):

        self.rect.y -= self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.top = block.rect.bottom

        if self.collide_with_enemy(enemies):
            self.rect.x = starting_x
            self.rect.y = starting_y

    def move_down(self, walls, enemies, starting_x, starting_y):

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:
            if self.change_y < 0:
              self.rect.bottom = block.rect.top

        if self.collide_with_enemy(enemies):
            self.rect.x = starting_x
            self.rect.y = starting_y

class Level(object):

    wall_list = None
    enemy_list = None
    starting_x = 0
    starting_y = 0

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()

class Level1(Level):
    def __init__(self):
        super().__init__()

        starting_x = 210 
        starting_y = 775 

        walls = [[0, 0, 20, 1000, WHITE],
                [1480, 0, 20, 1000, WHITE],
                [20, 0, 1500, 20, WHITE],
                [0, 980, 1500, 20, WHITE],
                [100, 100, 3, 700, WHITE],
                [100, 800, 1200, 3, YELLOW],
                [1300, 100, 3, 700, YELLOW],
                [100, 100, 250, 3, YELLOW],
                [350, 100, 3, 550, YELLOW],
                [350, 650, 90, 3, YELLOW],
                [450, 100, 3, 550, YELLOW],
                [450, 100, 850, 3, YELLOW]
                ]
        enemies = [[500, 410, 20, 375, BLUE, 300, 0],
                  ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4], item[5],
                item[6])
            self.enemy_list.add(enemy)

class Level2(Level):
    def __init__(self):
        super().__init__()

        starting_x = 225 
        starting_y = 775 

        walls = [[0, 0, 20, 1000, WHITE],
                [1480, 0, 20, 1000, WHITE],
                [20, 0, 1500, 20, WHITE],
                [0, 980, 1500, 20, WHITE],
                [150, 150, 3, 250, YELLOW],
                [150, 150, 1150, 3, YELLOW],
                [1300, 150, 3, 750, YELLOW],
                [150, 900, 1150, 3, YELLOW],
                [150, 650, 3, 250, YELLOW],
                [150, 650, 900, 3, YELLOW],
                [1050, 400, 3, 250, YELLOW],
                [150, 400, 900, 3, YELLOW]
                ]
        enemies = [[350, 770, 20, 20, BLUE, 0, -400],
                  [500, 770, 20, 20, BLUE, 0, 400],
                  [650, 770, 20, 20, BLUE, 0, -400],
                  [800, 770, 20, 20, BLUE, 0, 400],
                  [950, 770, 20, 20, BLUE, 0, -400],
                  [350, 250, 20, 20, BLUE, 0, 400],
                  [500, 250, 20, 20, BLUE, 0, -400],
                  [650, 250, 20, 20, BLUE, 0, 400],
                  [800, 250, 20, 20, BLUE, 0, -400],
                  [950, 250, 20, 20, BLUE, 0, 400],
                  ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4], item[5],
                item[6])
            self.enemy_list.add(enemy)

class Level3(Level):
    def __init__(self):
        super().__init__()

        starting_x = 200 
        starting_y = 895 

        walls = [[0, 0, 20, 1000, WHITE],
                [1480, 0, 20, 1000, WHITE],
                [20, 0, 1500, 20, WHITE],
                [0, 980, 1500, 20, WHITE],
                [150, 950, 1200, 6, YELLOW],
                [1350, 200, 6, 750, YELLOW],
                [1350, 200, 100, 6, YELLOW],
                [1450, 100, 6, 100, YELLOW],
                [250, 100, 1200, 6, YELLOW],
                [250, 100, 6, 750, YELLOW],
                [150, 850, 100, 6, YELLOW],
                [150, 850, 6, 100, YELLOW]
                ]

        enemies = [[780, 220, 40, 118, BLUE, -1000, 0],
                  [780, 340, 40, 118, BLUE, 1000, 0],
                  [780, 460, 40, 118, BLUE, -1000, 0],
                  [780, 580, 40, 118, BLUE, 1000, 0],
                  [780, 700, 40, 118, BLUE, -1000, 0],
                  ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4], item[5],
                item[6])
            self.enemy_list.add(enemy)

def main(genomes, config):

    pygame.init()

    levels = []

    level = Level1()
    levels.append(level)

    level = Level2()
    levels.append(level)

    level = Level3()
    levels.append(level)

    current_level_num = 0
    current_level = levels[current_level_num]

    player_sprites = pygame.sprite.Group()

    clock = pygame.time.Clock()

    done = False

    players = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(15,15))
        ge.append(genome)

        for player in players:
            player_sprites.add(player)

        while not done:
            dt = clock.tick(60) / 1000

            for enemy in current_level.enemy_list:
                enemy.enemymove(current_level.wall_list, dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    quit()
                    break

            for x, player in enumerate(players):

                ge[x].fitness += .01

                output = nets[players.index(player)].activate((player.rect.x, player.rect.y, player.get_closest_enemy(current_level.enemy_list), player.get_closest_wall(current_level.wall_list)))

                if output[0] > .5:
                    player.move_right(current_level.wall_list, current_level.enemy_list, current_level.starting_x, current_level.starting_y)
                elif output[1] > .5:
                    player.move_left(current_level.wall_list, current_level.enemy_list, current_level.starting_x, current_level.starting_y)
                elif output[2] > .5:
                    player.move_down(current_level.wall_list, current_level.enemy_list, current_level.starting_x, current_level.starting_y)
                elif output[3] > .5:
                    player.move_up(current_level.wall_list, current_level.enemy_list, current_level.starting_x, current_level.starting_y)

                if player.collide_with_enemy(current_level.enemy_list):
                    ge[players.index(player)].fitness -= 1
                    player.num_deaths += 1

                    if player.num_deaths() > 5:
                        ge[players.index(player)].fitness -= 5
                        nets.pop(players.index(player))
                        ge.pop(players.index(player))
                        players.pop(players.index(player))

            screen.fill(BLACK)
            player_sprites.draw(screen)
            current_level.wall_list.draw(screen)
            current_level.enemy_list.draw(screen) 
            pygame.display.flip()

            clock.tick(60)


def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
