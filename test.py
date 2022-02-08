import pygame
pygame.mixer.init()
pygame.mixer.Channel(9).play(pygame.mixer.Sound(r'.\assets\sounds\move.wav'))
print(pygame.mixer.get_num_channels())