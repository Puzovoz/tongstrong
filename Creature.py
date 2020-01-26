from Terrain import Terrain

import pygame

class Creature(pygame.sprite.Sprite):
  def __init__(self, x, y, size, color, max_speed):
    super().__init__()
    self.image = pygame.Surface([32, 32])
    self.image.fill(color)
    self.position = pygame.math.Vector2(x, y)
    self.rect = self.image.get_rect(x=x, y=y)
    
    self.inertia = pygame.math.Vector2(0, 0)
    self.max_speed = max_speed

    self.standing_on = None
  
  def fell_off_terrain(self):
    # Start falling if creature is not on terrain
    if self.standing_on and \
    not pygame.Rect.colliderect(self.rect.move([0, 1]), self.standing_on.rect):
      self.standing_on = None
      self._started_falling = pygame.time.get_ticks()
      return True
    return False    
  
  def decelerate(self, friction, t_delta):
    if self.inertia.x > 0: 
      self.inertia.x = max(0, self.inertia.x - friction/1000*t_delta)
    else:
      self.inertia.x = min(0, self.inertia.x + friction/1000*t_delta)
      
    if not self.jumping and not self.standing_on and self.inertia.y < 10:
      self.jumping = False
      gravity = 30
      self.inertia.y += gravity/1000 * t_delta    
  
  def terrain_collide(self):
    for terrain in pygame.sprite.spritecollide(self, Terrain.all, False):
      sides = [abs(self.rect.top - terrain.rect.bottom),  # Collided with bottom of obstacle
               abs(self.rect.bottom - terrain.rect.top),  # With top
               abs(self.rect.left - terrain.rect.right),  # With right side
               abs(self.rect.right - terrain.rect.left)]  # With left
      closest = sides.index(min(sides))

      if closest == 0:
        self.position.y = terrain.rect.bottom
        self.rect.top = terrain.rect.bottom
        return closest
      
      if closest == 1:
        self.position.y = terrain.rect.top - self.rect.height
        self.standing_on = terrain
        self.inertia.y = min(0, self.inertia.y)
        return closest
      
      if closest == 2:
        self.position.x = terrain.rect.right
        self.rect.left = terrain.rect.right
        return closest
      
      if closest == 3:
        self.position.x = terrain.rect.left - self.rect.width
        self.rect.right = terrain.rect.left
        return closest
      
      