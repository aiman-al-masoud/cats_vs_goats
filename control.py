#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 19:00:03 2021

@author: aiman
"""

import pygame



class LocalController():
    
    """
    LocalController takes in a MySprite and moves it around,
    based on what keys_pressed is passed to its update() method.
    """
    
    def __init__(self, sprite):
        self.sprite = sprite
        
    def update(self, keys_pressed):
        
        if keys_pressed[pygame.K_LEFT]:
            self.sprite.move("L")   
        if keys_pressed[pygame.K_RIGHT]:
            self.sprite.move("R")   
        if keys_pressed[pygame.K_UP]:
            self.sprite.move("U")   
        if keys_pressed[pygame.K_DOWN]:
            self.sprite.move("D")    
        if keys_pressed[pygame.K_SPACE]:
            self.sprite.move("S") 












