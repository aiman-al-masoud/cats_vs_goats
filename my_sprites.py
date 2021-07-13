#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 18:18:18 2021

@author: aiman
"""

import pygame, random

#CONSTANTS:
PLAYER_IMG_PATH ="cat.png" 
ENEMY_IMG_PATH = "goat.png"
BULLET_IMG_PATH = "fish.png"

#CUSTOM EVENTS
ENEMY_HIT = pygame.event.Event(pygame.USEREVENT, attr1 = "ENEMY_HIT")
PLAYER_WAS_HIT = pygame.event.Event(pygame.USEREVENT, attr1 = "PLAYER_WAS_HIT")
RESPAWN_ENEMY = pygame.event.Event(pygame.USEREVENT, attr1 = "RESPAWN_ENEMY")
GAME_OVER = pygame.event.Event(pygame.USEREVENT, attr1 = "GAME_OVER")


#A BASIC SPRITE THAT CAN MOVE AROUND AND CHECK FOR COLLISIONS
class MySprite():
    
   
    global CURRENT_WINDOW
    
    #needs image path, and initial coordinates
    def __init__(self, image_path, init_x, init_y):   
        self.DIRECTIONS = {"R" : self.right, "L" : self.left, "U" : self.up, "D": self.down}
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(init_x, init_y, self.image.get_width(), self.image.get_height())
        self.speed = 5
        self.current_direction = "R"


    def right(self):
    
        self.rect.x = self.rect.x+self.speed if  self.rect.x+self.speed < self.window.get_size()[0]  else    self.rect.x 
        self.current_direction = "R"
    
    def left(self):
        self.rect.x = self.rect.x  - self.speed if self.rect.x+self.speed > 0 else    self.rect.x 
        self.current_direction = "L"
    def up(self):
        self.rect.y = self.rect.y  - self.speed if  self.rect.y  - self.speed >0  else    self.rect.y
        self.current_direction = "U"
    def down(self):
        self.rect.y = self.rect.y+self.speed if  self.rect.y+self.speed < self.window.get_size()[1]  else    self.rect.y
        self.current_direction = "D"

    
    
    #updates the position of the sprite
    def move(self, direction):
        self.DIRECTIONS[direction]()
    
    #draws the sprite on the screen
    def render(self, window):

        self.window = window
        
        #change the orientation of the image for when walking in different directions
        hor_flip = False
        if self.current_direction == "L":
            hor_flip = True
            
            
        transf_image = pygame.transform.flip(self.image, hor_flip , False)
        
        
        window.blit(transf_image, (self.rect.x, self.rect.y))
        pygame.display.update()
    
    
    
    
    #checks if this sprite collided with another
    def is_colliding(self, other_sprite):
        return True if self.rect.colliderect(other_sprite.rect) == 1  else False
    
    def is_onscreen(self):
        
        if self.rect.x < 0 or self.rect.x > self.window.get_size()[0]  or  self.rect.y < 0 or self.rect.y > self.window.get_size()[1]  :         
            return False
        
        return True
    
    
    
    
#A SPRITE THAT *IS* A BULLET
class Bullet(MySprite):
    
    def __init__(self, init_x, init_y, direction):
        MySprite.__init__(self, BULLET_IMG_PATH, init_x, init_y)
        self.direction = direction
        self.speed = 40
        
    def soar(self):
        self.move(self.direction)
        
    def render(self, window):
       MySprite.render(self, window)
       self.soar()
       
        
        
        
        
    


#A SPRITE THAT CAN SHOOT A BULLET
class Shooter(MySprite):
    def __init__(self,image_path, init_x, init_y):
        MySprite.__init__(self, image_path, init_x, init_y)
        self.bullets  = []
        
    def shoot(self):
        
        if len(self.bullets) > 10:
            self.bullets.clear()
        
        new_bullet = Bullet(self.rect.x, self.rect.y, self.current_direction)
        self.bullets.append(new_bullet)
    
    def move(self, direction):
        
        #shoot
        if direction == "S":
            self.shoot()
            return
        
        #else do what superclass does
        MySprite.move(self,direction)
        
    
    def render(self, window):
        
        #render the shooter
        MySprite.render(self, window)
        
        #render its bullets
        for bullet in self.bullets:
            
            #draw the bullet
            bullet.render(window)
            
            #remove bullets that flew out of the screen
            if not bullet.is_onscreen():
                self.bullets.remove(bullet)
                
                
    def is_colliding(self, other_sprite):
        
        
        #check bullet collisions
        for bullet in self.bullets:
            if bullet.is_colliding(other_sprite):
                pygame.event.post(ENEMY_HIT)
                self.bullets.remove(bullet)
       
         
        #check sprite collisions 
        if MySprite.is_colliding(self, other_sprite):
            pygame.event.post(PLAYER_WAS_HIT)
            

                
            
    
    
        


#A SPRITE FOR THE MAIN PLAYER
class Player(Shooter):
    
    def __init__(self, init_x, init_y):
        Shooter.__init__(self, PLAYER_IMG_PATH, init_x, init_y)
        self.health = 100
        
    def hit(self):
        self.health-=1
        
        if self.health <= 0:
            pygame.event.post(GAME_OVER)
            
    
        
        
#A SPRITE FOR THE PLAYER'S ANTAGONIST
class Enemy(MySprite):
        
    def __init__(self, init_x, init_y):
        MySprite.__init__(self,ENEMY_IMG_PATH, random.randint(0, 400), random.randint(0, 400))
        self.health = 10
        self.to_next_choice = 100 
        self.direction = random.choice(["R", "L", "U", "D"])

        
    def hit(self):
        self.health-=1
        
        if self.health <= 0:
            pygame.event.post(RESPAWN_ENEMY)
        
    

    def update(self):
        
        if self.to_next_choice <= 0:
            self.direction = random.choice(["R", "L", "U", "D"])
            self.to_next_choice = 50
        
        
        self.move(self.direction)
        self.to_next_choice-=1    
        
        
        






