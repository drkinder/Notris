# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:24:40 2018

@author: Dylan
"""
import pygame

pygame.mixer.init()
'''
pygame.mixer.Channel(0).play(pygame.mixer.Sound('a.wav'))
pygame.mixer.Channel(1).play(pygame.mixer.Sound('c.wav'))
pygame.mixer.Channel(2).play(pygame.mixer.Sound('e.wav'))
'''

pygame.mixer.music.load("e.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("d.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("c.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("d.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("e.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("e.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("e.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("d.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("d.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("d.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("e.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("g.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

pygame.mixer.music.load("g.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue