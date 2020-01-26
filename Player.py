from Creature import Creature

import pygame.time

class Player(Creature):
  def __init__(self, x, y):
    super().__init__(x, y, size=[32, 32], color=(255, 0, 0), max_speed=5)
    self.movement_direction = 0
    
    self.jumping = False
    self.jumps_left = 2
    self._jumps = 2
    self._jump_height = 150
    self._last_jumped = 0
    
    self._speed = 0
    self.started_running = 0
  
  def move_left(self):
    self.movement_direction -= 1
    self.started_running = pygame.time.get_ticks()
    
  def move_right(self):
    self.movement_direction += 1
    self.started_running = pygame.time.get_ticks()
    
  def stop_moving_left(self):
    self.movement_direction += 1
    self.inertia.x = min(-self._speed, self.inertia.x)
    self._speed = 0
    
  def stop_moving_right(self):
    self.movement_direction -= 1
    self.inertia.x = max(self._speed, self.inertia.x)
    self._speed = 0
  
  def jump(self):
    if not self.jumps_left: return
    self.jumps_left -= 1
    self.jumping = True
    self.inertia.y = 0
    self._last_jumped = pygame.time.get_ticks()
    self.standing_on = None
    
  def stop_jumping(self):
    self.inertia.y = max(0, self.inertia.y)
    self.jumping = False
  
  def accelerate(self, duration, t_delta):
    self._speed = min(self.max_speed,
                      self._speed + self.max_speed/duration*t_delta)
    
  def process(self, t_delta):
    # Accelerate on user movement input
    if self.movement_direction and self._speed < self.max_speed:
      self.accelerate(100, t_delta)
    
    self.decelerate(30, t_delta)
    
    # Start falling if player is not on terrain
    if self.fell_off_terrain(): self.jumps_left -= 1
    
    # Jump processing
    jump_duration = (pygame.time.get_ticks() - self._last_jumped) / 500
    if self.jumping and jump_duration < 1:
      offset = self._jump_height * (1 - jump_duration) / 250 * t_delta
      self.position.y -= offset
    else:
      self.jumping = False
      
    
    self.position.x += self.movement_direction * self._speed * t_delta/(1000/60)
    self.position += self.inertia * t_delta/(1000/60)
    
    # Rect can only hold int values which is inconvenient for precise calculations,
    # so we store position in a different variable with floating point values.
    self.rect.topleft = self.position
    
    # If a player landed on top side of terrain, restore jumps 
    if self.terrain_collide() == 1:
      self.jumping = False
      self.jumps_left = self._jumps