#mythicon game page

#import####
import pygame,sys,random
from pygame import mixer
import mysql.connector

#highscore####
#login-info
f=open('mythicon_others/username.txt')
username=f.read()
f.close()
#connecting to mysql for old-highscore
mydb= mysql.connector.connect(host="localhost",user="root",passwd="dango@12345",database="mythiconlogin")
cur=mydb.cursor()
cur.execute('select * from login where username=%s',[(username)])
usertuple=cur.fetchall()
oldhighscore=usertuple[0][2]

#functions####
#floor
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,285))
    screen.blit(floor_surface,(floor_x_pos+739,285))
#cloudb
def create_cloudb():
    random_cloudb_pos = random.choice(cloudb_height)
    new_cloudb = cloudb_surface.get_rect(midtop = (1100,random_cloudb_pos))
    return new_cloudb

def move_cloudb(cloudbs):
    for cloud in cloudbs:
        cloud.centerx -= 2
    return cloudbs

def draw_cloudb(cloudbs):
    for cloudb in cloudbs:
        screen.blit(cloudb_surface,cloudb)
#cloudw
def create_cloudw():
    random_cloudw_pos = random.choice(cloudw_height)
    new_cloudw = cloudw_surface.get_rect(midtop = (800,random_cloudw_pos))
    return new_cloudw

def move_cloudw(cloudws):
    for cloud in cloudws:
        cloud.centerx -= 2
    return cloudws

def draw_cloudw(cloudws):
    for cloudw in cloudws:
        screen.blit(cloudw_surface,cloudw)

#collision
def check_collision(cloudbs):
    for cloudb in cloudbs:
        if dragon_rect.colliderect(cloudb):
            return False

    if dragon_rect.top <= -200 or dragon_rect.bottom >= 550:
        return False

    return True

#dragon
def dragon_animation():
    new_dragon = dragon_frames[dragon_index]
    new_dragon_rect = new_dragon.get_rect(center = (120,dragon_rect.centery))
    return new_dragon,new_dragon_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(0,0,0))
        score_rect = score_surface.get_rect(center = (369,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score            - {int(score)}' ,True,(0,0,0))
        score_rect = score_surface.get_rect(center = (620,40))
        screen.blit(score_surface,score_rect)
        high_score_surface = game_font.render(f'High score - {int(high_score)}',True,(0,0,0))
        high_score_rect = high_score_surface.get_rect(center = (620,70))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

#intialising pygame####
pygame.init()
screen= pygame.display.set_mode((739,415))
pygame.display.set_caption('MYTHICON')
clock = pygame.time.Clock()
game_font = pygame.font.Font('mythicon_others/ka1.ttf',20)

#game variables######
gravity = 0.25
dragon_movement=0
game_active= True

#score
score = 0
high_score = oldhighscore

#bg
bg_surface = pygame.image.load('mythicon_images/yell.jpg').convert()

#bg music
mixer.music.load('mythicon_sounds/valley.wav')
mixer.music.play(-1)

#floor
floor_surface = pygame.image.load('mythicon_images/refloor.png').convert_alpha()
floor_x_pos = 0

#dragon
drag0 = pygame.image.load('mythicon_images/drag/drag0.png').convert_alpha()
drag1 = pygame.image.load('mythicon_images/drag/drag1.png').convert_alpha()
drag2 = pygame.image.load('mythicon_images/drag/drag2.png').convert_alpha()
drag3 = pygame.image.load('mythicon_images/drag/drag3.png').convert_alpha()
drag4 = pygame.image.load('mythicon_images/drag/drag4.png').convert_alpha()
drag5 = pygame.image.load('mythicon_images/drag/drag5.png').convert_alpha()
drag6 = pygame.image.load('mythicon_images/drag/drag6.png').convert_alpha()
drag7 = pygame.image.load('mythicon_images/drag/drag7.png').convert_alpha()
drag8 = pygame.image.load('mythicon_images/drag/drag8.png').convert_alpha()
drag9 = pygame.image.load('mythicon_images/drag/drag9.png').convert_alpha()

dragon_frames = [drag0,drag1,drag2,drag3,drag4,drag5,drag6,drag7,drag8,drag9]
dragon_index = 0
dragon_surface = dragon_frames[dragon_index]
dragon_rect=dragon_surface.get_rect(center = (120,200))

DRAGONFLAP = pygame.USEREVENT +2
pygame.time.set_timer(DRAGONFLAP,100)

#cloudb
cloudb_surface = pygame.image.load('mythicon_images/black.png').convert_alpha()
cloudb_list =[]
SPAWNCLOUDB = pygame.USEREVENT
pygame.time.set_timer(SPAWNCLOUDB,2400)
cloudb_height = [70,110,200]
 
#cloudw
cloudw_surface = pygame.image.load('mythicon_images/white.png').convert_alpha()
cloudw_list = []
SPAWNCLOUDW = pygame.USEREVENT +1
pygame.time.set_timer(SPAWNCLOUDW,2400)
cloudw_height = [20,170,250]

#game over
game_over_surface= pygame.image.load('mythicon_images/game over.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center =(369,207))

#sounds
flap_sound = pygame.mixer.Sound('mythicon_sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('mythicon_sounds/dragon_roar_hit.wav')

#main game loop####
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #updating highscore to mysql table
            inthigh_score=int(high_score)
            if high_score>oldhighscore:
                cur.execute('update login set highscore=%s where username=%s',[(inthigh_score),(username)])
                mydb.commit()
            #exit button    
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                dragon_movement =0
                dragon_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                cloudb_list.clear()
                cloudw_list.clear()
                dragon_rect.center=(120,200)
                dragon_movement = 0
                score = 0
        if event.type == SPAWNCLOUDB:
            cloudb_list.append(create_cloudb())
        if event.type == SPAWNCLOUDW:
            cloudw_list.append(create_cloudw())
        if event.type == DRAGONFLAP:
            if dragon_index < 9:
                dragon_index+=1
            else:
                dragon_index = 0
                
            dragon_surface,dragon_rect = dragon_animation()
            
    #gamebg              
    screen.blit(bg_surface,(0,0))
    
    if game_active:
        playdeathonce=1
        #dragon
        dragon_movement += gravity
        dragon_rect.centery += dragon_movement
        screen.blit(dragon_surface,dragon_rect)
        game_active = check_collision(cloudb_list)
        #cloudbs
        cloudb_list =move_cloudb(cloudb_list)
        draw_cloudb(cloudb_list)
        #cloudws
        cloudw_list = move_cloudw(cloudw_list)
        draw_cloudw(cloudw_list)
        #score
        score+=0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        if playdeathonce == 1:
            death_sound.play()
            playdeathonce+=1
            
    #floor
    floor_x_pos-=3
    draw_floor()
    if floor_x_pos <= -739:
        floor_x_pos = 0
        
    pygame.display.update()
    clock.tick(120)
    
###########THE END##############


    
