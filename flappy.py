import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 550
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255,255,255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
minus_boost = False
plus_boost = False
game_over = False
pipe_gap = 200
pipe_frequency = 1500 #milliseconds
minus_frequency = 1250
plus_frequency = 900
last_pipe = pygame.time.get_ticks() - pipe_frequency
last_minus = pygame.time.get_ticks() - minus_frequency
last_plus = pygame.time.get_ticks() - plus_frequency
# minus_interval = 2000
# time_minus = 
score = 0
pass_pipe = False



#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')
plus_img = pygame.image.load('img/plus.png')
minus_img = pygame.image.load('img/minus.png')


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	score = 0
	return score


class Bird(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range (1, 4):
			img = pygame.image.load(f"img/bird{num}.png")
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):

		if flying == True:
			#apply gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			self.mid_air = True
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.mid_air == True:  
					self.vel = -10
					self.jumped = True
			if key[pygame.K_SPACE] == False:
					self.jumped = False


				#handle the animation
			flap_cooldown = 5
			self.counter += 1
			
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
				self.image = self.images[self.index]


			#rotate the bird
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			#point the bird at the ground
			self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/pipe.png")
		self.rect = self.image.get_rect()
		#position variable determines if the pipe is coming from the bottom or top
		#position 1 is from the top, -1 is from the bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		elif position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]


	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()


#klass för minus booster
class Minus(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/minus.png")
		self.rect = self.image.get_rect()
		self.rect.topleft= [x,y]


	def update(self):
		self.rect.x -= scroll_speed

		if self.rect.right < 0:
			self.kill()

#klass för plus booster
class Plus(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/plus.png")
		self.rect = self.image.get_rect()
		self.rect.topleft= [x,y]


	def update(self):
		self.rect.x -= scroll_speed

		if self.rect.right < 0:
			self.kill()		


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action



pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
minus_group = pygame.sprite.Group()
plus_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

#create rem button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


run = True
while run:

	clock.tick(fps)

	#draw background
	screen.blit(bg, (0,0))

	pipe_group.draw(screen)
	minus_group.draw(screen)
	plus_group.draw(screen)
	bird_group.draw(screen)
	bird_group.update()

	#draw and scroll the ground
	screen.blit(ground_img, (ground_scroll, 768))

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False
	draw_text(str(score), font, white, int(screen_width / 2), 20)


	#look for collision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True


	for bird, minus in pygame.sprite.groupcollide(bird_group, minus_group, False, False).items():
        # Reduce scroll speed
		scroll_speed = 2
    	# Remove the collided minus sprites from minus_group			
		for minus_sprite in minus:
				minus_sprite.kill()
	
	for bird, plus in pygame.sprite.groupcollide(bird_group, plus_group, False, False).items():
        # Reduce scroll speed
		scroll_speed = 6
    	# Remove the collided minus sprites from minus_group			
		for plus_sprite in plus:
				plus_sprite.kill()


	#once the bird has hit the ground it's game over and no longer flying   
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False


	if flying == True and game_over == False:
		
		#generate new pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now

		pipe_group.update()

		for i in range(2, 4):
			random_int = random.uniform(2, 3)

		time_minus = pygame.time.get_ticks()
		if time_minus - last_minus > minus_frequency:
			minus = Minus(screen_width, int(screen_height / random_int))
			minus_group.add(minus)
			last_minus = time_minus
		minus_group.update()

		time_plus = pygame.time.get_ticks()
		if time_plus - last_plus > plus_frequency:
			plus = Plus(screen_width, int(screen_height / random_int))
			plus_group.add(plus)
			last_plus = time_plus
		plus_group.update()
		

		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0
	

	#check for game over and reset
	if game_over == True:
		if button.draw():
			game_over = False
			score = reset_game()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()