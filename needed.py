import pygame
from assets import *

#controles
controls = {
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "LEFT": pygame.K_LEFT,
    "RIGHT": pygame.K_RIGHT,
    "INTERACT": pygame.K_e
}

#affichage
display_info = pygame.display.Info()
w, h = display_info.current_w, display_info.current_h
SCREEN = pygame.display.set_mode((w, h))
FULLSCREEN = False


#options
slider_music = Slider((1 * w)/4, (2 * h)/6, w/3, h/25, 0, 105.88, "Music volume")
slider_sfx = Slider((1 * w)/4, (3 * h)/6, w/3, h/20, 0, 105.88, "Effect volume")
slider_fps = Slider((1 * w)/4, (4 * h)/6, w/3, h/20, 0, 105.06,"FPS cap")

music_volume = 10
sfx_volume = 10
fps = slider_fps.value

# Dropdown menu options
options = ["800x600", "1024x768", "1280x720", "1366x768", "1600x900", "1680x1050"]
dropdown = Dropdown(20, 20, 150, 40, options)


#jeu
fps = 60
fpsClock = pygame.time.Clock()

BG = pygame.image.load("assets/BG_Game.jpg")

#varialbes du jeu
pistolet = False #Pour savoooir si le joueur peut utiliser ou non son pistolet
doudou = True #Pour savoir si le joueur a encoree son  doudou ou non
père = True #Pour voir si le père retrouve la fille ou pas à la fin
blessée = False #Condition pour savoir si le joueur a interagis avce le chien
sprite_pistolet = True
détective = True
chien = True
vieux = True
Truands = True

AA = False
Fin_1 = False #epuisement
Fin_2 = False #suicide
Fin_3 = False #pinoccio
Fin_4 = False #Happy end :)
Fin_5 = False #retour vie de famille
Fin_6 = False #parmis les truands
Fin = False


#sons
menu_music = "./assets/sounds/musics/menu_music.wav"
game_music = "./assets/sounds/musics/game_music.wav"
giga_chad = "./assets/sounds/musics/giga_chad.wav"
fin_vieux = "./assets/sounds/musics/fin_vieux.wav"
fin_truands = "./assets/sounds/musics/fin_truands.wav"

sfx_jump = pygame.mixer.Sound("./assets/sounds/sfx/jump.mp3")
sfx_walking = pygame.mixer.Sound('./assets/sounds/sfx/walking.mp3')


#fonctions
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(None, size)