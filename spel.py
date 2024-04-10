import pygame
import sys
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 300
SCREEN_SIZE = (WIDTH, HEIGHT)

# Colors
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Game Start Screen")

# Load background image
background_image = pygame.image.load("Background (2).jpg").convert()

# Fonts
font = pygame.font.SysFont(None, 48)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Draw title text
        draw_text("Behind the forest", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)

        # Draw instructions
        draw_text("Press ENTER to start", font, BLACK, screen, WIDTH // 2, HEIGHT // 2)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(30)

# Run the start screen
start_screen()

screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Endless Scroll")

#load image
bg = pygame.image.load("Gamebackground (1).jpg").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

#define game variables
scroll = 0
tiles = math.ceil(WIDTH  / bg_width) + 1

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw scrolling background
  for i in range(0, tiles):
    screen.blit(bg, (i * bg_width + scroll, 0))
    bg_rect.x = i * bg_width + scroll
    
  #scroll background
  scroll -= 3

  #reset scroll
  if abs(scroll) > bg_width:
    scroll = 0

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

  

pygame.quit()
# Once the start screen is closed, the game loop will start here
