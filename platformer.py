from Player import Player
from Terrain import Terrain

import pygame

import random
from enum import Enum, auto

pygame.init()
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode((800, 600))
game_surface = screen.copy()
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

class _Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super().__call__(*args, **kwargs)
    return cls._instances[cls]

class GameState(Enum):
  GAME = auto()
  MENU = auto()
  MAP = auto()

class Game(object, metaclass=_Singleton):
  def __init__(self):
    self.game_state = GameState.GAME
    self.done = False
    self.screen_offset = pygame.math.Vector2(0, 0)
    self.player = pygame.sprite.GroupSingle(Player(200, 318))
  
  def toggle_menu(self):
    if self.game_state in [GameState.GAME, GameState.MENU]:
      self.game_state = GameState.GAME if self.game_state == GameState.MENU else GameState.MENU
      
  def toggle_map(self):
    if self.game_state in [GameState.GAME, GameState.MAP]:
      self.game_state = GameState.GAME if self.game_state == GameState.MAP else GameState.MAP
  
  def run(self):
    Terrain(200, 350, 400, 50)
    Terrain(200, 230, 150, 50)
    Terrain(450, 230, 150, 50)
    
    while not self.done:
      
      ### INPUT PROCESSING
      
      keys = pygame.key.get_pressed()
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.done = True
          
        # Processing keys
        if event.type in [pygame.KEYDOWN, pygame.KEYUP] and \
           event.key in Controls:
          Controls[event.key][event.type-2]()
          
        # Processing mouse
        mouse = pygame.mouse.get_pos()
      
      
      
      ########
      
      ### RENDERING
      
      # Game state      
      if self.game_state == GameState.GAME:
        screen.fill(BGCOLOR)
        game_surface.fill(BGCOLOR)
        
        # Move screen depending on mouse position
        self.screen_offset.xy = [(screen.get_width()  / 2 - mouse[0]) / 3,
                                 (screen.get_height() / 2 - mouse[1]) / 3]
        
        if self.screen_offset.magnitude() > 150:
          self.screen_offset = self.screen_offset.normalize() * 150
          
        self.screen_offset.xy += [screen.get_width()/2, screen.get_height()/2]
        self.screen_offset.xy -= Game().player.sprite.rect.topleft
        
        for terrain in Terrain.all:
          game_surface.blit(terrain.image, terrain.rect)
        
        self.player.sprite.process(clock.get_time())
        game_surface.blit(self.player.sprite.image, self.player.sprite.rect)
        
        screen.blit(game_surface, self.screen_offset)
      
      
      
      # Menu state
      if self.game_state == GameState.MENU:
        screen.fill((0, 255, 255))
      
      
      
      pygame.display.flip()
      clock.tick(120)

class IterableControls(type):
  def __iter__(cls):
    return iter(cls._keys)
  
  def __getitem__(cls, item):
    return cls._keys[item]

class Controls(metaclass=IterableControls):
  p = Game().player.sprite
  
  _keys = {
    pygame.K_w: (p.jump, p.stop_jumping),
    pygame.K_a: (p.move_left, p.stop_moving_left),
    pygame.K_d: (p.move_right, p.stop_moving_right),
    pygame.K_m: (Game().toggle_map, Game().toggle_map),
    pygame.K_ESCAPE: (lambda: None, Game().toggle_menu)
  }

if __name__ == "__main__":
  game = Game()
  game.run()
  pygame.quit()

