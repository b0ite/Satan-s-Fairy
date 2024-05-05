import pygame, sys, pygame.freetype, os
from assets import *
from needed import *
from play import *

pygame.init()
pygame.display.set_caption("Menu")

# Initialize the mixer module
pygame.mixer.init()

# Détermine si le script est exécuté en mode 'congelé' par PyInstaller
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Chemin vers le dossier des assets
assets_path = os.path.join(application_path, 'assets')


font = pygame.freetype.SysFont("Arial", 20)

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


def options():
    global controls, music_volume, sfx_volume, fps, w, h, slider_fps, slider_music, slider_sfx, SCREEN, dropdown, options, FULLSCREEN

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        fond = pygame.image.load('./assets/Menu/BG_Options.png').convert()
        fond = pygame.transform.scale(fond, (w, h))
        SCREEN.blit(fond, (0, 0))

        #definir le contenu du texte
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS SCREEN.", True, "white")
        #definir la position de la hitbox du texte
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((w/2), (h/10)))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        slider_music.draw(SCREEN)
        slider_sfx.draw(SCREEN)
        slider_fps.draw(SCREEN)


        en_attente = False

        OPTIONS_BACK = Button(image=None, pos=(((6*w)/7), ((57*h)/60)), 
                            text_input="Back", font=get_font(75), base_color="white", hovering_color="pink")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        OPTIONS_UP = Button(image=None, pos=(((6*w)/7), ((1*h)/6)), 
                            text_input="Up", font=get_font(75), base_color="white", hovering_color="pink")
        OPTIONS_UP.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_UP.update(SCREEN)

        OPTIONS_DOWN = Button(image=None, pos=(((6*w)/7), ((2*h)/6)), 
                            text_input="Down", font=get_font(75), base_color="white", hovering_color="pink")
        OPTIONS_DOWN.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_DOWN.update(SCREEN)

        OPTIONS_LEFT = Button(image=None, pos=(((6*w)/7), ((3*h)/6)), 
                            text_input="Left", font=get_font(75), base_color="white", hovering_color="pink")
        OPTIONS_LEFT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_LEFT.update(SCREEN)

        OPTIONS_RIGHT = Button(image=None, pos=(((6*w)/7), ((4*h)/6)), 
                            text_input="Right", font=get_font(75), base_color="white", hovering_color="pink")
        OPTIONS_RIGHT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RIGHT.update(SCREEN)

        OPTIONS_INTERACT = Button(image=None, pos=(((6*w)/7), ((5*h)/6)), 
                            text_input="Interact", font=get_font(75), base_color="white", hovering_color="pink")
        OPTIONS_INTERACT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_INTERACT.update(SCREEN)

        OPTIONS_FULLSCREEN = Button(image=None, pos=(((1*w)/7), ((6*h)/7)), 
                            text_input="Fullscreen", font=get_font(75), base_color="white", hovering_color="pink")
        OPTIONS_FULLSCREEN.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_FULLSCREEN.update(SCREEN)


        KEY_TEXT = get_font(80).render("Saisir une touche", True, "white")
        KEY_RECT = KEY_TEXT.get_rect(center=((w/2), (h/2)))


        for event in pygame.event.get():
            music_volume = slider_music.value
            sfx_volume = slider_sfx.value
            display_info = pygame.display.Info()
            w = display_info.current_w
            h = display_info.current_h

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                print("window resized")
                slider_music.update_dimensions(w, h, relative_x=1/4, relative_y=2/6, relative_width= 1/3, relative_height=1/25)
                slider_sfx.update_dimensions(w, h, relative_x=1/4, relative_y=3/6, relative_width= 1/3, relative_height=1/25)
                slider_fps.update_dimensions(w, h, relative_x=1/4, relative_y=4/6, relative_width= 1/3, relative_height=1/25)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

                #mapping des touches
                if OPTIONS_UP.checkForInput(OPTIONS_MOUSE_POS):
                    en_attente = True
                    print("saisir une touche")
                    SCREEN.blit(KEY_TEXT, KEY_RECT)
                    pygame.display.flip()
                    while en_attente:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                controls["UP"] = event.key
                                print(controls["UP"])
                                en_attente = False
                if OPTIONS_DOWN.checkForInput(OPTIONS_MOUSE_POS):
                    en_attente = True
                    print("saisir une touche")
                    SCREEN.blit(KEY_TEXT, KEY_RECT)
                    pygame.display.flip()
                    while en_attente:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                controls["DOWN"] = event.key
                                print(controls["DOWN"])
                                en_attente = False
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    en_attente = True
                    print("saisir une touche")
                    SCREEN.blit(KEY_TEXT, KEY_RECT)
                    pygame.display.flip()
                    while en_attente:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                controls["LEFT"] = event.key
                                print(controls["LEFT"])
                                en_attente = False
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    en_attente = True
                    print("saisir une touche")
                    SCREEN.blit(KEY_TEXT, KEY_RECT)
                    pygame.display.flip()
                    while en_attente:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                controls["RIGHT"] = event.key
                                print(controls["RIGHT"])
                                en_attente = False
                if OPTIONS_INTERACT.checkForInput(OPTIONS_MOUSE_POS):
                    en_attente = True
                    print("saisir une touche")
                    SCREEN.blit(KEY_TEXT, KEY_RECT)
                    pygame.display.flip()
                    while en_attente:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                controls["INTERACT"] = event.key
                                print(controls["INTERACT"])
                                en_attente = False
                if OPTIONS_FULLSCREEN.checkForInput(OPTIONS_MOUSE_POS):
                    if FULLSCREEN == False :
                        SCREEN = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
                        FULLSCREEN = True
                    else :
                        SCREEN = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                        FULLSCREEN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown.is_open:
                # Check if click is on any option
                    for i in range(len(dropdown.options)):
                        rect = pygame.Rect(dropdown.x, dropdown.y + dropdown.height * (i + 1), dropdown.width, dropdown.option_height)
                        if rect.collidepoint(event.pos):
                            dropdown.selected_index = i
                            pygame.display.set_mode((int(dropdown.options[i].split('x')[0]), int(dropdown.options[i].split('x')[1])), pygame.RESIZABLE)
                            dropdown.is_open = False
                            slider_music.update_dimensions(w, h, relative_x=1/4, relative_y=2/6, relative_width= 1/3, relative_height=1/25)
                            slider_sfx.update_dimensions(w, h, relative_x=1/4, relative_y=3/6, relative_width= 1/3, relative_height=1/25)
                            slider_fps.update_dimensions(w, h, relative_x=1/4, relative_y=4/6, relative_width= 1/3, relative_height=1/25)
                            break
                else:
                    rect = pygame.Rect(dropdown.x, dropdown.y, dropdown.width, dropdown.height)
                    if rect.collidepoint(event.pos):
                        dropdown.is_open = not dropdown.is_open
            slider_music.handle_event(event)
            slider_sfx.handle_event(event)
            slider_fps.handle_event(event)
                    # Set the volume for music and sound effects
            pygame.mixer.music.set_volume((music_volume/100)-0.01)  # music_volume ranges from 0.0 to 1.0
            sfx_jump.set_volume((sfx_volume/100)-0.01)  # sfx_volume ranges from 0.0 to 1.0

        dropdown.draw(SCREEN)
        pygame.display.update()
        fpsClock.tick(fps)

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

def main_menu():
    global controls, music_volume, sfx_volume, fps, w, h
    while True:
        fond = pygame.image.load('./assets/BG_Game.jpg').convert()
        fond = pygame.transform.scale(fond, (w, h))
        SCREEN.blit(fond, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=((w/2), (h/6)))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Menu/Play Rect.png"), pos=((w/2), (h/4)), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Menu/Options Rect.png"), pos=((w/2), (h/2.5)), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Menu/Quit Rect.png"), pos=((w/2), (h/1.8)), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            display_info = pygame.display.Info()
            w = display_info.current_w
            h = display_info.current_h
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    fade_to_black(SCREEN)
                    lower_volume()
                    print("c'est censé jouer")
                    play()                    
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    fade_to_black(SCREEN)
                    lower_volume()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        fpsClock.tick(fps)

# Start playing the background music
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)  # -1 for looping indefinitely
main_menu()