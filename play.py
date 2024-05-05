import pygame, sys
from needed import *
from assets import *
from pygame.locals import *
from dialogues import *

hauteur = 9*h/10 #c'est ma hauteur du sol

#La class générale sprite
class sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx):
        super().__init__()
        if image is not None:
            self.image = pygame.image.load(image).convert_alpha()
            self.rect = self.image.get_rect()
        else:
            self.image = None  # L'image est à spécifier ailleurs
            self.rect = pygame.Rect(0, 0, 0, 0)  # Initialize with an empty rect
        self.rect.bottomleft = [startx, hauteur]
    
    def update(self, *args, **kwargs):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class player(sprite):
    def __init__(self, startx, screen_width, screen_height):
        super().__init__(None, startx)  # Call the parent class (sprite) constructor without an image
        # Load the idle and walking frames, now directly into the player's constructor
        self.idle_frames = [adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_1.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_1 copie.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_2.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_2 copie.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_3.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_3 copie.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_4.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_4 copie.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_5.png').convert_alpha()),
                            adapt_player_scale(pygame.image.load('./assets/Girl_Idle/Idle_5 copie.png').convert_alpha())]
        
        self.walking_frames = [adapt_player_scale(pygame.image.load('./assets/Girl_Walking/Walking_1.png').convert_alpha()),
                               adapt_player_scale(pygame.image.load('./assets/Girl_Walking/Walking_2.png').convert_alpha()),
                               adapt_player_scale(pygame.image.load('./assets/Girl_Walking/Walking_3.png').convert_alpha()),
                               adapt_player_scale(pygame.image.load('./assets/Girl_Walking/Walking_4.png').convert_alpha())]
        
        self.jumping_frames = [adapt_player_scale(pygame.image.load('./assets/Girl_Walking/Walking_3.png').convert_alpha())]
        # Initialize the image and rect based on the idle frame
        self.frame_index = 0
        self.image = self.idle_frames[self.frame_index]
        # Redimensionner les images en fonction de la taille de l'écran
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [startx, hauteur]
        self.can_move_d = True #utile pour empêcher les déplacements lors du scroll droite -> gauche
        self.can_move_g = True #utile pour empêcher les déplacements lors du scroll gauche -> droite
        self.dialoging = False #utile pour empêcher les déplacements lors du dialogue
        self.facing_right = True  # Définir la direction initiale du personnage
        self.speed = 1
        self.y_speed = 0
        self.jumping = False
        self.gravity = 0.05  
        self.jump_speed = -3.5  
        self.jump_height = 100
        self.animation_time = 0
        self.animation_speed = 150  # in milliseconds

    def update(self, keys, current_time):
        moving = False
        if self.can_move_d and self.can_move_g and not self.dialoging:
            if (keys[controls["UP"]] and not self.jumping):
                if self.facing_right == True and (keys[pygame.K_LEFT] or keys[controls["LEFT"]]): # Si le personnage fait face à droite, retournez toutes les images
                    self.flip_sprites()
                if self.facing_right != True and (keys[pygame.K_RIGHT] or keys[controls["RIGHT"]]): # Si le personnage fait face à gauche, retournez toutes les images
                    self.flip_sprites()
                    self.flip_sprites()
                sfx_walking.stop()  # Stop walking sound on jump
                self.y_speed = self.jump_speed
                self.jumping = True
                sfx_jump.play()
                self.current_frames = self.jumping_frames
            if (keys[pygame.K_LEFT] or keys[controls["LEFT"]]) and self.rect.x > 0:
                if self.facing_right:  # Si le personnage fait face à droite, retournez toutes les images
                    self.flip_sprites()
                self.rect.x -= self.speed
                moving = True
                self.current_frames = self.walking_frames
            elif (keys[pygame.K_RIGHT] or keys[controls["RIGHT"]]):
                if not self.facing_right:  # Si le personnage fait face à gauche, retournez toutes les images
                    self.flip_sprites()
                self.rect.x += self.speed
                moving = True
                self.current_frames = self.walking_frames
            else:
                self.current_frames = self.idle_frames

        # Animation handling
        if moving:
            self.current_frames = self.walking_frames
        else:
            self.current_frames = self.idle_frames
        if self.jumping:
            self.current_frames = self.jumping_frames

        # Update the animation frame if enough time has passed
        if current_time - self.animation_time > self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.frame_index]
            self.animation_time = current_time

        # Conserver la position actuelle lors de la mise à jour du rect
        current_bottomleft = self.rect.bottomleft
        self.rect = self.image.get_rect()
        self.rect.bottomleft = current_bottomleft

        #pour le saut:
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.y_speed < 0 and self.rect.bottom <= self.jump_height:
            self.y_speed = 0
            self.jumping = False

        if self.rect.bottom >= hauteur:
            self.rect.bottom = hauteur
            self.jumping = False
            self.y_speed = 0
    
    def flip_sprites(self):
        # Retourne horizontalement toutes les images des frames
        self.idle_frames = [pygame.transform.flip(frame, True, False) for frame in self.idle_frames]
        self.walking_frames = [pygame.transform.flip(frame, True, False) for frame in self.walking_frames]
        self.jumping_frames = [pygame.transform.flip(frame, True, False) for frame in self.jumping_frames]
        self.facing_right = not self.facing_right  # Change la direction du personnage

    def draw(self, screen):
        self.kill()
        screen.blit(self.image, self.rect)

#______________________________________________________________________________________________________
class objets_interactifs(sprite):
    def __init__(self, image_path, startx, étiquette, screen_width, screen_height):
        global hauteur #on garde le sol
        super().__init__(image_path, startx)
        self.name = étiquette #On associe à chaque objet un nom/une étiquette unique qui sera utile pour les dialogues
        if image_path is not None:
            self.image = adapt_scale(pygame.image.load(image_path).convert_alpha())
            '''if self.image is not None:  # Vérifiez si l'image a été chargée avec succès
                self.image = pygame.transform.scale(self.image,
                                                     (int(self.image.get_width() * (screen_width / (screen_width + 200))),
                                                      int(self.image.get_height() * (screen_height / (screen_height + 200)))))
                self.rect = self.image.get_rect(bottomleft=(startx, hauteur))
            else:
                self.image = None
                self.rect = pygame.Rect(0, 0, 0, 0)'''
            self.rect = self.image.get_rect(bottomleft=(startx, hauteur))
        else:
            self.image = None
            self.rect = pygame.Rect(0, 0, 0, 0)
        #Au dessus on modifie les sprites  en fonction de la taille de la fenêtre de jeu

    def update(self, keys, current_time):
        pass
    
    def draw(self, screen):
        if self.image is not None:  # Vérifiez si une image existe avant de dessiner
            screen.blit(self.image, self.rect)
            self.rect.bottom = hauteur



#__________________________________________________________________________________________________________
def play():
    global hauteur, Fin_1, Fin_2, Fin_3, Fin_4, Fin_5, Fin_6, pistolet, doudou, père, blessée, Truands, détective, chien, vieux, Fin, sprite_pistolet, AA
    #informations de l'ecran et definition de la fenetre de jeu
    display_info = pygame.display.Info()
    w = display_info.current_w
    h = display_info.current_h

    scrolling = False #scroll droite -> gauche
    scrolling2 = False #scroll gauche -> droite
    impasse = True #pour empêcher le scroll quand le jeu commence

    #ici on place le timer des animations
    pygame.time.set_timer(pygame.USEREVENT, 100)


    all_sprites = pygame.sprite.Group() #groupe qui contient tous les sprites
    interactive_objects = pygame.sprite.Group() #groupe pour tous les objets interactifs


    #Ici on initialise les objets :
    s_player = player(0, w, h)  # Crée une instance de la classe player
    obj = objets_interactifs('./assets/personnages/Quentin_the_caillou.png', 6*w, "photo", w, h)  # Crée une instance de la classe objets_interactifs
    obj_2 = objets_interactifs('./assets/personnages/Ivan_the_caillou.png', w*(6+2/4), "Lampadaire", w, h)
    tonneau = objets_interactifs('./assets/perso.png', w*(6 + 1/6), "Tonneau ?", w, h)
    prop_papa = objets_interactifs('./assets/personnages/pere_full.png', 4*w, "Papa", w, h)
    prop_detective = objets_interactifs('./assets/personnages/detective_full.png', w*(2+1/6.1), "detective", w, h)
    prop_truands = objets_interactifs('./assets/personnages/Truands.png', w*(1 + 1/6.8), "truands", w, h)
    prop_vieux = objets_interactifs('./assets/personnages/Vieux.png', w*(2 + 3/4), "vieux", w, h)
    prop_chien = objets_interactifs('./assets/personnages/chien_full.png', w*(3+1/2), "chien", w, h)
    prop_pistolet = objets_interactifs('./assets/personnages/pistolet.png', w/6, "pistolet", w, h)
    prop_gamin = objets_interactifs('./assets/personnages/Gamin.png', w*(1 + 1/7), "Gamin", w, h)
    prop_banc = objets_interactifs('./assets/Props/banc.png', w*(2 + 3/4), "Banc", w, h)
    prop_maison = objets_interactifs('./assets/Props/maison.png', -w, "maison", w, h)

    #Pour le scrolling
    scroll = 0

    #debug du probleme de dialogues
    un = False #pistolet
    deux = False #truands
    trois = False #chien
    quatre = False #detective
    cinq = False #papa
    six = False #vieux
    sept = False #egg

    #Ici on ajoute les objets inittialisés dans les groupes de sprites pour la gestion de ces derniers et des collisions
    interactive_objects.add(obj, obj_2, tonneau, prop_papa, prop_detective, prop_truands, prop_vieux, prop_chien, prop_pistolet, prop_gamin, prop_banc, prop_maison)
    all_sprites.add(s_player, obj, obj_2, tonneau, prop_papa, prop_detective, prop_truands, prop_vieux, prop_chien, prop_pistolet, prop_gamin, prop_banc, prop_maison)

    #tests :
    print(obj.rect.bottomleft)
    print(s_player.rect.bottomleft)
    print(controls["UP"])
    print(controls["DOWN"])
    print(controls["LEFT"])
    print(controls["RIGHT"])
    print("jeu en cours")

    #Initialisation du background en jeu et des bg de fins:
    fond = pygame.image.load('./assets/BG_Game.jpg').convert()
    fond = pygame.transform.scale(fond, (w, h))
    bg_Fin_1 = pygame.image.load('./assets/Image de fin/FIN_1_Epuisements.png').convert()
    bg_Fin_1 = pygame.transform.scale(bg_Fin_1, (w, h))
    bg_Fin_2 = pygame.image.load('./assets/Image de fin/FIN_2.png').convert()
    bg_Fin_2 = pygame.transform.scale(bg_Fin_2, (w, h))
    bg_Fin_3 = pygame.image.load('./assets/Image de fin/FIN_3_Pinocchio.png').convert()
    bg_Fin_3 = pygame.transform.scale(bg_Fin_3, (w, h))
    bg_Fin_4 = pygame.image.load('./assets/Image de fin/FIN_4_Happy_End.png').convert()
    bg_Fin_4 = pygame.transform.scale(bg_Fin_4, (w, h))
    bg_Fin_5 = pygame.image.load('./assets/Image de fin/FIN_5_Retour_vie_famille.png').convert()
    bg_Fin_5 = pygame.transform.scale(bg_Fin_5, (w, h))
    bg_Fin_6 = pygame.image.load('./assets/Image de fin/FIN_6_Parmi_les_truands.png').convert()
    bg_Fin_6 = pygame.transform.scale(bg_Fin_6, (w, h))
    


    #On lance l'intro du jeu dès que le play() se lance
    dialogue_system.trigger_dialogue("intro")

    # Assuming pygame.mixer is already initialized
    channel = pygame.mixer.find_channel()  # Find an available channel
    if channel is not None:
        channel.play(sfx_walking, loops=-1)
    else:
        print("No available audio channels!")

    channel.stop()


    #on lance la musique
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)  # -1 for looping indefinitely
    #_______________________________________________________________________________
    while True:
        SCREEN.blit(fond, (0, 0))
        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        #PLAY_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            dialogue_system.handle_event(event)
            if event.type == pygame.USEREVENT:  # This event occurs every 100 milliseconds
                s_player.update(keys, current_time)  # Update the player
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key in [pygame.K_RIGHT, pygame.K_LEFT]) and not s_player.jumping:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    if channel is None or not channel.get_busy():  # Ensure the channel is free or not busy
                        channel = pygame.mixer.find_channel()
                        if channel is not None:
                            channel.play(sfx_walking, loops=-1)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    if channel is not None:
                        channel.stop()
            if dialogue_system.active:
            # Check if the player made a choice in the dialogue
                if event.type == pygame.KEYDOWN:
                    # Check if a choice triggered an event
                    if dialogue_system.triggered_event:
                        if dialogue_system.triggered_event == "pistolet":
                            pistolet = False
                        if dialogue_system.triggered_event == "take_pistolet":
                            sprite_pistolet = False
                            pistolet = True
                        if dialogue_system.triggered_event == "pistoletsuppr":
                            sprite_pistolet = False
                        if dialogue_system.triggered_event == "pistochien":
                            pistolet = False
                            chien = False
                            blessée = True
                        if dialogue_system.triggered_event == "Fin_1":
                            Fin_1 = True
                        if dialogue_system.triggered_event == "Fin_2":
                            Fin_2 = True
                        if dialogue_system.triggered_event == "Fin_3":
                            Fin_3 = True
                        if dialogue_system.triggered_event == "Fin_4":
                            Fin_4 = True
                            #init musique
                            pygame.mixer.music.load(fin_vieux)
                            pygame.mixer.music.play(-1)  # -1 for looping indefinitely
                        if dialogue_system.triggered_event == "Fin_5":
                            Fin_5 = True
                        if dialogue_system.triggered_event == "Fin_6":
                            Fin_6 = True
                            #init musique
                            pygame.mixer.music.load(fin_truands)
                            pygame.mixer.music.play(-1)  # -1 for looping indefinitely
                        if dialogue_system.triggered_event == "doudou":
                            doudou = False
                            détective = False
                            père = False
                        if dialogue_system.triggered_event == "père":
                            père = False
                        if dialogue_system.triggered_event == "blessée":
                            blessée = True
                            chien = False
                        if dialogue_system.triggered_event == "vieux":
                            vieux = False
                        if dialogue_system.triggered_event == "tuer_pap":
                            père = False
                            pistolet = False
                        if dialogue_system.triggered_event == "Truands":
                            Truands = False
                        if dialogue_system.triggered_event == "fuite_det":
                            détective = False
                        if dialogue_system.triggered_event == "tuer_det":
                            pistolet = False
                            détective = False
                        dialogue_system.reset_triggered_event()
            if event.type == KEYDOWN and (event.key == K_e or keys[controls["INTERACT"]]):
                # Vérifie la proximité entre le joueur et l'objet interactif
                collided_sprites = pygame.sprite.spritecollide(s_player, interactive_objects, False)
                #Pour le lancement des dialogues
                for objet in collided_sprites:
                    print(objet.name)  # Tests pour voir les interactions
                    if pygame.sprite.collide_rect(s_player, prop_pistolet) and not un:
                        dialogue_system.trigger_dialogue("Le player trouve le pistolet")#on lance le bon dialogue
                        un = True
                    #elif pygame.sprite.collide_rect(s_player, obj_2):
                        #dialogue_system.trigger_dialogue("object2")
                    #elif pygame.sprite.collide_rect(s_player, tonneau):
                       # dialogue_system.trigger_dialogue("object3")
                    if pygame.sprite.collide_rect(s_player, prop_truands):
                        if pistolet :
                            dialogue_system.trigger_dialogue("Rencontre avec les truands(pistolet)")
                        else:
                            dialogue_system.trigger_dialogue("Rencontre avec les truands(sans pistolet)")
                    if pygame.sprite.collide_rect(s_player, prop_chien) and not trois:
                        trois = True
                        if pistolet:
                            dialogue_system.trigger_dialogue("Rencontre avec chien (avec pistolet)")
                        else:
                            dialogue_system.trigger_dialogue("Rencontre avec chien (sans pistolet)")
                    elif pygame.sprite.collide_rect(s_player, prop_vieux) and not six:
                        six = True
                        if not père and blessée and peluche:
                            dialogue_system.trigger_dialogue("Rencontre avec les vieux (bon)")
                        else:
                            dialogue_system.trigger_dialogue("Rencontre avec les vieux (pas bon)")

            meet_sprites = pygame.sprite.spritecollide(s_player, interactive_objects, False)
            for sprite in meet_sprites:
                if pygame.sprite.collide_rect(s_player, prop_maison):
                            s_player.rect.x += 30
                            dialogue_system.trigger_dialogue("Rentrer_Maison")
                if pygame.sprite.collide_rect(s_player, prop_detective) and not quatre:
                    quatre = True
                    if père and pistolet:
                        dialogue_system.trigger_dialogue("detective avec pistolet")
                    elif père and not pistolet:
                        dialogue_system.trigger_dialogue("detective sans pistolet")
                elif pygame.sprite.collide_rect(s_player, prop_papa) and not cinq:
                        cinq = True
                        if pistolet:
                            dialogue_system.trigger_dialogue("papa pistolet")
                        else:
                            dialogue_system.trigger_dialogue("papa sans pistolet")
                elif pygame.sprite.collide_rect(s_player, obj_2) and not sept:
                    sept = True
                    pygame.mixer.music.load(giga_chad)
                    pygame.mixer.music.play(-1)  # -1 for looping indefinitely
                    dialogue_system.trigger_dialogue("Egg")

            if event.type == pygame.VIDEORESIZE:
                w, h = event.size
                for elements in all_sprites :
                    x = elements.rect.x
                    elements.rect.bottomleft = (x, 3*h/4)   # Recalculer la position du joueur et de l'objet interactif lors du redimensionnement de la fenêtre
        #_____________________________________________________________________________Scroll
        # Vérifiez si le joueur est arrivé à la partie de l'écran où le scrolling doit être déclenché
        if s_player.rect.right >= w * 9 / 10:
            scrolling = True

        if scrolling:
            s_player.can_move_d = False            
            for sprite in all_sprites:
                sprite.rect.x -= 6  # Ajuste la position horizontale des sprites
            scroll -= 6
            
            # Réinitialisation du défilement si nécessaire
        if s_player.rect.left <= w * 1/ 2:
            scrolling = False
            s_player.can_move_d = True
        if s_player.rect.left > w*1/2:
            impasse = False
        #impasse empêche le premier scrolling
        #___________________________________________________________________________________________________________
        #Scroll quand le joueur arrive à gauche de l'écran (marche :) )
        if s_player.rect.left <= w * 1 / 10:
            scrolling2 = True

        if scrolling2 and impasse == False:
            s_player.can_move_g = False
            for sprite in all_sprites:
                sprite.rect.x += 6  # Ajuste la position horizontale des sprites
            scroll += 6


        # Dessin de l'arrière-plan en ajustant la position en fonction du scrolling
        for i in range(-1, 2):
            if scrolling or s_player.rect.x >0 and not Fin:
                SCREEN.blit(fond, (fond.get_width() * i + scroll, 0))
            elif scrolling2 and not Fin:
                SCREEN.blit(fond, (fond.get_width() * i + scroll, 0))
        
        # Réinitialisation du défilement si nécessaire
        if abs(scroll) > fond.get_width():
            scroll = 0
                                
        # Réinitialisation du défilement si nécessaire
        if s_player.rect.right > w * 1/2:
            scrolling2 = False
            s_player.can_move_g = True

        #Condition pour la fin 1:
        if not père and not vieux and not Truands and not sprite_pistolet:
            Fin_1 = True
        #Ici condition pour lancer fin:
        if Fin_1:
            if not Fin:
                for elem in interactive_objects:
                    elem.kill()
                pygame.display.flip()
            Fin = True
            if not s_player.dialoging and not AA:
                fond = bg_Fin_1
                dialogue_system.trigger_dialogue("Fin_1")
                AA = True
        elif Fin_2:
            if not Fin:
                for elem in interactive_objects:
                    elem.kill()
                pygame.display.flip()
            Fin = True
            if not s_player.dialoging and not AA:
                fond = bg_Fin_2
                dialogue_system.trigger_dialogue("Fin_2")
                AA = True
        elif Fin_3:
            if not Fin:
                for elem in interactive_objects:
                    elem.kill()
                pygame.display.flip()
            Fin = True
            if not s_player.dialoging and not AA:
                fond = bg_Fin_3
                dialogue_system.trigger_dialogue("Fin_3")
                AA = True
        elif Fin_4:
            if not Fin:
                for elem in interactive_objects:
                    elem.kill()
                pygame.display.flip()
            Fin = True
            if not s_player.dialoging and not AA:
                fond = bg_Fin_4
                dialogue_system.trigger_dialogue("Fin_4")
                AA = True
        elif Fin_5:
            if not Fin:
                for elem in interactive_objects:
                    elem.kill()
                pygame.display.flip()
            Fin = True
            if not s_player.dialoging and not AA:
                fond = bg_Fin_5
                dialogue_system.trigger_dialogue("Fin_5")
                AA = True
        elif Fin_6:
            if not Fin:
                for elem in interactive_objects:
                    elem.kill()
                pygame.display.flip()
            Fin = True
            if not s_player.dialoging and not AA:
                fond = bg_Fin_6
                dialogue_system.trigger_dialogue("Fin_6")
                AA = True
        else:
            #Condition pour la suppression des sprites:
            if père == False:
                prop_papa.kill()
            else:
                prop_papa.draw(SCREEN)
            
            if sprite_pistolet == False:
                prop_pistolet.kill()
            else:
                prop_pistolet.draw(SCREEN)

            if chien == False:
                prop_chien.kill()
            else:
                prop_chien.draw(SCREEN)

            if vieux == False:
                prop_banc.draw(SCREEN)
                prop_vieux.kill()
            else:
                prop_banc.draw(SCREEN)
                prop_vieux.draw(SCREEN)

            if détective == False or père == False:
                prop_detective.kill()
            else:
                prop_detective.draw(SCREEN)

            if Truands == False:
                prop_gamin.draw(SCREEN)
                prop_truands.kill()
            else:
                prop_truands.draw(SCREEN)
                prop_gamin.draw(SCREEN)
            #ici on dessine les sprites et on les updates
            obj.draw(SCREEN)
            prop_maison.draw(SCREEN)
            obj_2.draw(SCREEN)
            tonneau.draw(SCREEN)
            s_player.draw(SCREEN)  # Dessinez le joueur
        all_sprites.add(s_player)
        all_sprites.update(keys, current_time)
        s_player.update(keys, current_time)



        #affichage des dialogues, doit etre le plus bas du code pour etre prioritaire à l'affichage
        if dialogue_system.active:
            s_player.dialoging = True 
            dialogue_system.draw()
        else:
            s_player.dialoging = False    
        pygame.display.flip()


'''
crash si fleche + barre espace pendant un choix

proleme avec les interactions dans certaines situations
exemple : interactions avec les bandits, les ignorer, tuer le chien, parler aux vieux, dialogue des bandits se déclenche (solved)
exemple : 002 et papa deviennent le pistolet si on revient en arriere dans le jeu (solved)
exemple : sans le pistolet apres l'intervention diplomatique impossible de fuir'''