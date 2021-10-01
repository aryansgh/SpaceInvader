import pygame
import random 
import math
import time

from pygame import mixer
#initialize pygame
 
pygame.init()

#create a screen
width = 800
height = 600

screen = pygame.display.set_mode((width, height))

#event: anything that happens in the game window

#background
background = pygame.image.load('spacebackground.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

#Adding background and title and icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png') #32*32 image
pygame.display.set_icon(icon)

#Adding player image
playerImg = pygame.image.load('player_spaceship.png')
playerX = width - 30 #approximately half width of the screen
playerY = height * 0.8 #the player spaceship will be in the lower half 
playerX_change = 0

#adding the enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('alien.png'))
	enemyX.append(random.randint(0,width - 65))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(-3)
	enemyY_change.append(40)

#adding bullet

#ready state: bullet not available
#fire state: bullet has been fired

bulletImg = pygame.image.load('bullet.png')
bulletX = random.randint(0,width)
bulletY = height * 0.8
bulletX = 0
bullet_state ="ready"
bulletY_change = 10

main_enemy = pygame.image.load('alien_enemy.png')
main_enemy_bullet = pygame.image.load('main_enemy_bullet.png')
main_enemyX = 250
main_enemyY = 60
main_enemyX_change = -3

main_enemy_bullet_X=0
main_enemy_bullet_Y=100
main_enemy_bulletY_change=10
main_enemy_bullet_state="ready"

#score value
score_value=0
font = pygame.font.Font('RooseSally.ttf',32)
game_over_font = pygame.font.Font('RooseSally.ttf',64)
textX=10
textY=10

def main_enemy_fire(x,y):
	global main_enemy_bullet_state
	main_enemy_bullet_state = "fire"
	screen.blit(main_enemy_bullet, (x+25,y+20))

def main_enemy_render(x,y):
	screen.blit(main_enemy, (x,y))

def game_over_text():
	game_over = game_over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(game_over, (260,250))

def show_score(x,y):
	score = font.render("Score :"+str(score_value),True,(255,255,255))
	screen.blit(score, (x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i], (x, y))

def player(x,y):
	screen.blit(playerImg, (x, y)) #drawing the player on the screen

def fire_bullet(x,y):
	global bullet_state
	bullet_state= "fire"
	screen.blit(bulletImg, (x+16, y+10)) #so tha bullet appears on the center of the spaceship

def burst_mode(x,y):
	global bullet_state
	bullet_state="burst"
	screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distanceX = math.pow(enemyX-bulletX, 2)
	distanceY = math.pow(enemyY-bulletY, 2)
	distance = math.sqrt(distanceX+distanceY)
	return distance

#game loop
running = True
while running:
	#adding background
	screen.fill((0, 0, 0)) #rgb 0-255

	#adding background
	screen.blit(background, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT: #game window closes when the cross button in pressed
			running = False

		# if keystroke is pressed check whether its right or left

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT: #checking if the left key is being pressed
				#print("left arrow is pressed")
				playerX_change = -5
			if event.key == pygame.K_RIGHT:
				#print("right key is being pressed")
				playerX_change = 5

			if event.key ==  pygame.K_SPACE:
				if bullet_state is "ready":
					bulletX  = playerX
					fire_bullet(playerX, bulletY)
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
			

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
				#print("Keystroke was released") 


	playerX += playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= width - 64:
		playerX = width - 64

	#checking the location of the enemy
	for i in range(num_of_enemies):
		#game over

		if enemyY[i]>=440:
			for j in range(num_of_enemies):
				enemyY[j]=2000

			game_over_text()
			break

		if enemyX[i] <= 0:
			enemyX_change[i] = 3
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= width - 64:
			enemyX_change[i] = -3
			enemyY[i] += enemyY_change[i]
		enemyX[i] += enemyX_change[i]

		distance = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if distance <=27 :
			bulletY = height * 0.8
			bullet_state = "ready"
			enemyX[i] = random.randint(0,width - 65)
			enemyY[i] = random.randint(50,150)
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			score_value += 1
			#print(score)

		enemy(enemyX[i],enemyY[i],i)

	if main_enemyX<=0:
		main_enemyX_change=3
	elif main_enemyX>=width - 64:
		main_enemyX_change=-3

	main_enemyX=main_enemyX+main_enemyX_change

	if main_enemy_bullet_Y>=height:
		main_enemy_bullet_state="ready"
		main_enemy_bullet_Y=60

	if main_enemy_bullet_state is "ready":
		main_enemy_bullet_X=main_enemyX
		main_enemy_fire(main_enemy_bullet_X,main_enemy_bullet_Y)

	if main_enemy_bullet_state is "fire":
		main_enemy_fire(main_enemy_bullet_X,main_enemy_bullet_Y)
		main_enemy_bullet_Y+=main_enemy_bulletY_change

	distance = isCollision(playerX, playerY, main_enemy_bullet_X, main_enemy_bullet_Y)
	if distance <=27 :
		playerY = height * 3 + height/3
		for j in range(num_of_enemies):
			enemyY[j]=height * 3 + height / 3

		game_over_text()

	if bulletY <= 0:
		#global bullet_state
		bulletY = height * 0.8
		bullet_state = "ready"


	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player(playerX, playerY)
	show_score(textX,textY)
	main_enemy_render(main_enemyX,main_enemyY)
	#enemy(enemyX, enemyY)
	pygame.display.update() #update the screen continuously

