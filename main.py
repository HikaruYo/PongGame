import pygame, sys, random

# Animasi bola
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, computer_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
        
    # Player Score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
        
    # Computer Score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        computer_score += 1
        score_time = pygame.time.get_ticks()
        
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        
    if ball.colliderect(computer) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - computer.right) < 10:
            ball_speed_x *= -1
            
# Animasi player
def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

# Animasi Computer
def computer_ai():
    if computer.top < ball.y:
        computer.top += computer_speed
    if computer.bottom > ball.y:
        computer.bottom -= computer_speed
    if computer.top <= 0:
        computer.top = 0
    if computer.bottom >= screen_height:
        computer.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y, current_time, score_time, number_three
    
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)
    
    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
        
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
    
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))
    
    if current_time - score_time <2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None
    
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

# Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# display
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Tampilan bola, player, dan computer
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 15, 15)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 90)
computer = pygame.Rect(10, screen_height/2 - 70, 10, 90)

# Warna
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Speed
ball_speed_x = 8 * random.choice((1, -1))
ball_speed_y = 8 * random.choice((1, -1))
player_speed = 0
computer_speed = 10

# Score teks
player_score = 0
computer_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 30)

score_time = True

# Sound
pong_sound = pygame.mixer.Sound("StoneDropping.mp3")
score_sound = pygame.mixer.Sound("ScoreUp.mp3")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thanks For Playing!")
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
            
    ball_animation()
    player_animation()
    computer_ai()
       
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, computer)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
    
    if score_time:
        ball_start()
    
    player_text = game_font.render(f"Player = {player_score}", False, light_grey)
    screen.blit(player_text, (660,470))
    
    computer_text = game_font.render(f"Computer = {computer_score}", False, light_grey)
    screen.blit(computer_text, (160,470))
    
    if player_score | computer_score >= 10:
        print("Game Finished!")
        print("Computer Score : " + str(computer_score))
        print("Player Score : " + str(player_score))
        print("Thanks For Playing!")
        pygame.quit()
        sys.exit()
    
    pygame.display.flip()
    clock.tick(60)
