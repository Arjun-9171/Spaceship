import pygame, random, time
from pygame import mixer

pygame.init()
screen_width = 1280
screen_height = 720
display_screen = pygame.display.set_mode((screen_width, screen_height))

rocket = pygame.image.load('rocket.png')
rocket = pygame.transform.scale(rocket, (100, 100))
#rocket = pygame.transform.rotate(rocket, -90)

#Break

enemy_spaceship = pygame.image.load('Enemy_spaceship.png')
enemy_spaceship = pygame.transform.scale(enemy_spaceship, (80, 80))
#enemy_spaceship = pygame.transform.rotate(enemy_spaceship)
enemy_x_pos = 900
enemy_y_pos = 300
enemy_spaceship_rect = enemy_spaceship.get_rect()
#Break
#Break

spaceship = pygame.image.load('Spaceship.png')
spaceship = pygame.transform.scale(spaceship, (100, 100))
spaceship = pygame.transform.rotate(spaceship, -90)
spaceship_x_pos = 200
spaceship_y_pos = 300
spaceship_rect = spaceship.get_rect()

#Break

rocket_x_pos = 200
rocket_y_pos = 300
rocket_speed = 0
triggered = False
rocket_rect = rocket.get_rect()

#Break 
mixer.init()
global lazer
lazer = mixer.Sound('Assets/lazer.mp3')
lazer.set_volume(0.05)
global soundtrack
soundtrack = mixer.music.load('POTC_song.mp3')
lives = 6
#font_for_lives = pygame.font.SysFont("Timesnewroman.fft", 50)

#Break

points = 0
font = pygame.font.SysFont("Timesnewroman.fft", 50)

def respawn_enemy():
  enemy_y_pos = random.randint(1, 670)
  enemy_x_pos = 1300
  return[enemy_x_pos, enemy_y_pos]

def respawn_rocket():
  triggered = False
  respawn_rocket_x = spaceship_x_pos
  respawn_rocket_y = spaceship_y_pos
  rocket_speed = 0
  return[triggered, respawn_rocket_x, respawn_rocket_y, rocket_speed]

def collision(): 
  global points
  global lives
  if spaceship_rect.colliderect(enemy_spaceship_rect):
    lives -= 1
    return True
  elif rocket_rect.colliderect(enemy_spaceship_rect):
    points += 1
    pos = [enemy_x_pos, enemy_y_pos]
    explosion = Explosion(pos[0], pos[1])
    explosion_group.add(explosion)
    hitbox.shoot()
    return True
  else:
    return False

class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for num in range (1, 6):
      img = pygame.image.load(f"Assets/explosions_imgs/Explosion{num}.png")
      img = pygame.transform.scale(img, (125, 75))
      self.images.append(img)
    self.index = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.counter = 0
 

  def update(self):
    explosion_speed = 15
    self.counter += 1
    if self.counter >= explosion_speed and self.index < len(self.images) - 1:
      self.counter = 0
      self.index += 1
      self.image = self.images[self.index]
    
    if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
      self.kill()

start_background = pygame.image.load('start_menu.jpg')
start_background = pygame.transform.scale(start_background, (screen_width, screen_height))
main_menu_font = pygame.font.SysFont("Timesnewroman.fft", 100)
main_menu = True
while main_menu:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
  main_menu_text = main_menu_font.render("Press F to Start", True, (30, 208, 194))
  display_screen.blit(start_background, (0, 0))
  display_screen.blit(main_menu_text, (375, 360))
  key = pygame.key.get_pressed()
  if key[pygame.K_f]:
    break
  pygame.display.update()

mixer.init()
mixer.music.play()

class Hitbox(pygame.sprite.Sprite):
  def __init__ (self,picture_path):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    self.lazer = pygame.mixer.Sound("Assets/lazer.mp3")
  def shoot(self):
    self.lazer.play()
  def update(self):
    self.rect.center=pygame.mouse.get_pos()

hitbox = Hitbox("Assets/hitbox.jpg")
hitbox_group = pygame.sprite.Group()
hitbox_group.add(hitbox)

explosion_group = pygame.sprite.Group()

background = pygame.image.load('BG_image.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False  
      exit() 
 
  display_screen.blit(background, (0, 0))
  screen_moving = screen_width % background.get_rect().width
  display_screen.blit(background, (screen_moving - background.get_rect().width, 0))
  explosion_group.draw(display_screen)
  explosion_group.update()
  if screen_moving < 1280:
    display_screen.blit(background, (screen_moving, 0))
    
  key = pygame.key.get_pressed()
  if key[pygame.K_w] and spaceship_y_pos > 1:
    spaceship_y_pos = spaceship_y_pos - 1
    if not triggered:
      rocket_y_pos = rocket_y_pos - 1
    
  if key[pygame.K_s] and spaceship_y_pos < 630:
    spaceship_y_pos = spaceship_y_pos + 1
    if not triggered:
      rocket_y_pos = rocket_y_pos + 1

  if key[pygame.K_SPACE]:
    triggered = True
    rocket_speed = 10
    mixer.Sound.play(lazer)

    
  
   

  if rocket_x_pos > 1300:
    triggered, rocket_x_pos, rocket_y_pos, rocket_speed = respawn_rocket()
  
  if enemy_x_pos <= -60:
    lives -= 1
    enemy_x_pos = respawn_enemy()[0]
    enemy_y_pos = respawn_enemy()[1]
  
  if collision():
    enemy_x_pos = respawn_enemy()[0]
    enemy_y_pos = respawn_enemy()[1]
  
  
  game_over_font = pygame.font.SysFont("Timesnewroman.fft", 100)
  if lives == 0:
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    display_screen.blit(game_over_text, (400, 300))
    pygame.display.update()
    pygame.time.delay(3000)  
    run = False
    
   
  


  spaceship_rect.x = spaceship_x_pos
  enemy_spaceship_rect.x = enemy_x_pos
  rocket_rect.x = rocket_x_pos
  spaceship_rect.y = spaceship_y_pos
  enemy_spaceship_rect.y = enemy_y_pos
  rocket_rect.y = rocket_y_pos

  screen_width = screen_width - 0.7
  rocket_x_pos = rocket_x_pos + rocket_speed
  enemy_x_pos = enemy_x_pos - 2
  
  #pygame.draw.rect(display_screen, 'red', spaceship_rect, 5)
  #pygame.draw.rect(display_screen, 'red', enemy_spaceship_rect, 5)
  #pygame.draw.rect(display_screen, 'red', rocket_rect, 5)

  score = font.render(f'Points: {int(points)}', True, "green")
  hearts = font.render(f'Lives: {int(lives)}', True, "red")

  display_screen.blit(score, (10, 10))
  display_screen.blit(hearts, (1140, 10))
  display_screen.blit(rocket, (rocket_x_pos, rocket_y_pos))
  display_screen.blit(spaceship, (spaceship_x_pos, spaceship_y_pos))
  display_screen.blit(enemy_spaceship, (enemy_x_pos, enemy_y_pos))



  
  pygame.display.update()
pygame.quit()