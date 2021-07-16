import pygame, my_sprites, control, os

#IS THE APP RUNNING?
RUNNING = True

#DIMENSIONS OF THE WINDOW
WIDTH, HEIGHT = 700,700
#GET THE WINDOW
WINDOW = pygame.display.set_mode( (WIDTH, HEIGHT) )

#THE GAME'S FPS
FPS = 60
#THE GAME'S CLOCK
CLOCK = pygame.time.Clock()
#GAMEOVER IMAGE
GAME_OVER_IMG = pygame.image.load("res"+os.sep+"game_over.png")
#GAME OVER FLAG
GAME_OVER = False
#score = goats taken down
SCORE = 0


#CREATE THE PLAYER'S SPRITE:
player = None
#CREATE THE ENEMY'S SPRITE:
enemy = None
#make a controller to control the player via the keyboard
player_conroller = None






#EXIT THE APP
def exit_app():
    global RUNNING
    RUNNING = False
    exit()
    
#HANDLE KEY EVENTS    
def handle_keys():    
    keys_pressed = pygame.key.get_pressed()
    player_conroller.update(keys_pressed)    
    

#print the game-over screen
def print_game_over():
    WINDOW.blit(GAME_OVER_IMG, (WIDTH/2, HEIGHT/2))
    pygame.display.update()    
    

#initialize objects for new game
def start_new_game():
    
    global player, enemy, player_conroller, SCORE
    
    #CREATE THE PLAYER'S SPRITE:
    player = my_sprites.Player(0,0)
    #CREATE THE ENEMY'S SPRITE:
    enemy = my_sprites.Enemy(100, 100)
    #make a controller to control the player via the keyboard
    player_conroller = control.LocalController(player)
    #re-initialize score to zero
    SCORE = 0

    
#update the game score
def update_game_score():
    pygame.display.set_caption("YOUR HP: "+str(player.health)+"  |  GOAT'S HP: "+str(enemy.health)+" | GOATS TAKEN DOWN: "+str(SCORE)   )
    
    
    
    

#start a new game    
start_new_game()    

    
# THE MAIN LOOP
while RUNNING:
    
    
    #if it's game-over, interrupt the current game, wait a little, then start a new game
    if GAME_OVER:
        print_game_over()
        pygame.time.delay(1000)
        start_new_game()
        GAME_OVER = False
        
        
    
    
    #DRAW THE SCREEN
    WINDOW.fill( (255,255,255) )
    
    #draw the player's sprite
    player.render(WINDOW)
       
    #draw the enemy's sprite
    enemy.render(WINDOW)

 
    #update the enemy's sprite
    enemy.update()

    #UPDATE THE SCREEN
    pygame.display.update()
    
    #check collisions
    player.is_colliding(enemy)
    
    #update the game score
    update_game_score()
    
    #SET THE CLOCK'S FPS
    CLOCK.tick(FPS)


    #CHECK FOR ANY SINGLE-EVENTS
    for event in pygame.event.get():
        
       #HANDLE QUIT EVENT 
       if event.type == pygame.QUIT:
           exit_app()
        
       #HANDLE ENEMY-HIT EVENT
       if event == my_sprites.ENEMY_HIT:
           enemy.hit()
           print(enemy.health)
        
       #HANDLE PLAYER_WAS_HIT EVENT
       if event == my_sprites.PLAYER_WAS_HIT:
          player.hit()
       
       #HANDLE ENEMY-RESPAWN EVENT
       if event == my_sprites.RESPAWN_ENEMY:
           enemy = my_sprites.Enemy(0,0)
           SCORE +=1
        
        
       #HANDLE GAMEOVER EVENT
       if event == my_sprites.GAME_OVER:
           GAME_OVER = True
        
    #HANDLE MULTIPLE KEY-EVENTS
    handle_keys()
    
    
   









    
    







    


