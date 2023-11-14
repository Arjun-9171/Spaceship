import pygame

pygame.init()
display_screen = pygame.display.set_mode((1280, 720))

lazer = pygame.image.load('Lazer.png')
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (1280, 720))
spaceship = pygame.image.load('Spaceship.png')
spaceship = pygame.transform.scale(spaceship, (100, 100))
spaceship = pygame.transform.rotate(spaceship, -90)
spaceship_x_pos = 200
spaceship_y_pos = 300
run = True
while run:
  display_screen.blit(background, (0,0))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  key = pygame.key.get_pressed()
  if key[pygame.K_w]:
    spaceship_y_pos = spaceship_y_pos - 0.6
  if key[pygame.K_s]:
    spaceship_y_pos = spaceship_y_pos + 0.6
  

  display_screen.blit(spaceship, (spaceship_x_pos, spaceship_y_pos))
  pygame.display.update()
pygame.quit()
