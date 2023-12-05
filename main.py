import pygame, random

pygame.init()
screen_width = 1280
screen_height = 720
display_screen = pygame.display.set_mode((screen_width, screen_height))

lazer = pygame.image.load('Lazer.png')
lazer = pygame.transform.scale(lazer, (30, 30))
lazer = pygame.transform.rotate(lazer, -90)

#Break

enemy_spaceship = pygame.image.load('Enemy_spaceship.gif')
enemy_spaceship = pygame.transform.scale(enemy_spaceship, (145, 145))
enemy_spaceship = pygame.transform.rotate(enemy_spaceship, 90)
enemy_x_pos = 900
enemy_y_pos = 300
#Break

background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))

#Break

spaceship = pygame.image.load('Spaceship.png')
spaceship = pygame.transform.scale(spaceship, (100, 100))
spaceship = pygame.transform.rotate(spaceship, -90)
spaceship_x_pos = 200
spaceship_y_pos = 300

#Break

lazer_x_pos = 245
lazer_y_pos = 335
lazer_speed = 0
triggered = False

def respawn_enemy():
  enemy_y_pos = random.randint(1, 715)
  enemy_x_pos = 1300
  return[enemy_y_pos, enemy_x_pos]

def respawn_lazer():
  triggered = False
  respawn_lazer_x = spaceship_x_pos
  respawn_lazer_y = spaceship_y_pos
  lazer_speed = 0
  return[triggered, respawn_lazer_x, respawn_lazer_y, lazer_speed]


  


run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  display_screen.blit(background, (0, 0))
  screen_moving = screen_width % background.get_rect().width
  display_screen.blit(background, (screen_moving - background.get_rect().width, 0))

  if screen_moving < 1280:
    display_screen.blit(background, (screen_moving, 0))
  key = pygame.key.get_pressed()
  if key[pygame.K_w] and spaceship_y_pos > 1:
    spaceship_y_pos = spaceship_y_pos - 1
    if not triggered:
      lazer_y_pos = lazer_y_pos - 1
    
  if key[pygame.K_s] and spaceship_y_pos < 630:
    spaceship_y_pos = spaceship_y_pos + 1
    if not triggered:
      lazer_y_pos = lazer_y_pos + 1

  if key[pygame.K_SPACE]:
    triggered = True
    lazer_speed = 10

  if lazer_speed > 1300:
    triggered, respawn_lazer_x, respawn_lazer_y, lazer_speed = respawn_lazer()
  
  if enemy_x_pos < 0:
    enemy_y_pos = respawn_enemy()[0]
    enemy_x_pos = respawn_enemy()[1]

  screen_width = screen_width - 0.7
  lazer_x_pos = lazer_x_pos + lazer_speed
  enemy_x_pos = enemy_x_pos - 1

  display_screen.blit(spaceship, (spaceship_x_pos, spaceship_y_pos))
  display_screen.blit(lazer, (lazer_x_pos, lazer_y_pos))
  display_screen.blit(enemy_spaceship, (enemy_x_pos, enemy_y_pos))
 

  
  pygame.display.update()
pygame.quit()
