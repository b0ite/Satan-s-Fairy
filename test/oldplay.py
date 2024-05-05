# Importation de pygame et des modules nécessaires
import pygame, sys
from needed import *
from assets import *

pygame.init()
# Définition de la fonction play
def play():
    while True:
        # Récupération de la position de la souris
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Gestion des événements pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Affichage du fond d'écran
        fond = pygame.image.load('./assets/BG_Game.png').convert()  # Chargement et conversion de l'image
        fond = pygame.transform.scale(fond, (w, h))  # Redimensionnement de l'image
        SCREEN.blit(fond, (0, 0))  # Affichage du fond d'écran

        pygame.display.flip()  # Rafraîchissement de l'écran

        fpsClock.tick(fps)  # Contrôle de la fréquence de rafraîchissement

        # Définition de la classe sprite
        class sprite(pygame.sprite.Sprite):
            def __init__(self, image, startx, starty):
                super().__init__()
                self.image = pygame.image.load(image)
                self.rect = self.image.get_rect()
                self.rect.center = [startx, starty]
            def update(self):
                pass
            def draw(self, screen):
                screen.blit(self.image, self.rect)

        # Définition de la classe player qui hérite de sprite
        class player(sprite):
            def __init__(self, startx, starty):
                super().__init__("Player.png", startx, starty)