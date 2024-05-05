import pygame

# Initialiser Pygame
pygame.init()

# Créer la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Charger l'image de fond
background_image = pygame.image.load('./assets/BG_Game.png')

# Obtenir la hauteur de la fenêtre
window_height = screen.get_height()

# Calculer le nouveau ratio de l'image pour garder le rapport hauteur/largeur
image_width = background_image.get_width()
image_height = background_image.get_height()
new_width = int((window_height / image_height) * image_width)

# Redimensionner l'image
resized_background = pygame.transform.scale(background_image, (new_width, window_height))

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner le fond adapté à la hauteur
    screen.blit(resized_background, (screen_width / 2 - new_width / 2, 0))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
