import pygame.sprite

class Terrain(pygame.sprite.Sprite):
  all = pygame.sprite.Group()
  def __init__(self, x, y, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill((0, 0, 0))
    self.rect = self.image.get_rect(x=x, y=y)
    
    self.all.add(self)