import pygame, math
from needed import *

class Dialogue:
    def __init__(self, screen, font_path, font_size=32, background_opacity=128):
        self.screen = screen
        self.dialogue_font = pygame.font.Font(font_path, font_size)
        self.name_font = pygame.font.Font(font_path, 25)
        self.choice_font = pygame.font.Font(font_path, 50)
        self.dialogues = {}
        self.current_dialogue = None
        self.dialogue_index = 0
        self.background_opacity = background_opacity
        self.active = False
        self.animation_offset = 0  # Décalage initial pour l'animation
        self.animation_direction = 0.3  # Direction de l'animation
        self.selected_choice = 0  # Index of the selected choice
        self.triggered_event = None
        self.sound_played = False  # Track if the sound has been played for the current dialogue
        pygame.mixer.init()
        self.character_sounds = {
            'Maman': pygame.mixer.Sound('./assets/sounds/sfx/maman_sound.mp3'),
            'Papa': pygame.mixer.Sound('./assets/sounds/sfx/papa_sound.mp3'),
            'Moi': pygame.mixer.Sound('./assets/sounds/sfx/player_sound.mp3')
        }

    def add_dialogue(self, key, dialogues):
        self.dialogues[key] = dialogues

    def trigger_dialogue(self, key):
        if key in self.dialogues:
            self.current_dialogue = self.dialogues[key]
            self.dialogue_index = 0
            self.active = True
            self.sound_played = False  # Reset sound played flag when a new dialogue is triggered
            self.update_choices()

    def draw(self):
        if not self.active or not self.current_dialogue:
            return
        
        # Mise à jour du décalage d'animation
        self.animation_offset += self.animation_direction * 2  # Vitesse de l'animation
        if abs(self.animation_offset) > 10:  # Amplitude de l'animation
            self.animation_direction *= -1  # Inverser la direction à l'amplitude max/min
        
        background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        background.set_alpha(self.background_opacity)
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))

        # Current step in dialogue
        step = self.current_dialogue[self.dialogue_index]
        
        # Checking if the current step has choices
        if isinstance(step, dict) and 'choices' in step:
            # Draw choices
            choice_height = 550  # Starting height for choices
            for idx, choice in enumerate(step['choices']):
                color = (255, 0, 0) if idx == self.selected_choice else (255, 255, 255)
                choice_text = self.choice_font.render(choice['text'], True, color)
                self.screen.blit(choice_text, (100, choice_height))
                choice_height += 50  # Increment to position next choice below
        else:
            # Process normal dialogue entries
            dialogue_rect = pygame.Rect(50, self.screen.get_height() - 150, self.screen.get_width() - 100, 100)
            
            for character in step:
                character_name, portrait, dialogue, position, is_speaking = character
                positions = {
                    'left': (50, self.screen.get_height() - portrait.get_height() - 100),
                    'center_left': (self.screen.get_width() // 4 - portrait.get_width() // 2, self.screen.get_height() - portrait.get_height() - 100),  # 1/4th from the left
                    'center': (self.screen.get_width() // 2 - portrait.get_width() // 2, self.screen.get_height() - portrait.get_height() - 100),
                    'center_right': (3 * self.screen.get_width() // 4 - portrait.get_width() // 2, self.screen.get_height() - portrait.get_height() - 100),  # 3/4th from the left
                    'right': (self.screen.get_width() - portrait.get_width() - 50, self.screen.get_height() - portrait.get_height() - 100)
                }
                if is_speaking:
                    # Apply animation to the character who is speaking
                    adjusted_position = (positions[position][0], positions[position][1] + self.animation_offset)
                    #play character sound
                    if character_name in self.character_sounds and not self.sound_played:
                        self.character_sounds[character_name].play()
                        self.sound_played = True  # Mark the sound as played
                else:
                    adjusted_position = positions[position]
                
                portrait_rect = portrait.get_rect(topleft=adjusted_position)
                self.screen.blit(portrait, portrait_rect)
                
                if is_speaking:
                    # Draw name background and text
                    name_text = self.name_font.render(character_name, True, (255, 255, 255))
                    name_background_rect = name_text.get_rect(x=adjusted_position[0], y=adjusted_position[1] - 30)
                    name_background_rect.inflate_ip(20, 10)  # Expand the rectangle for aesthetics
                    pygame.draw.rect(self.screen, (0, 0, 0), name_background_rect)  # Black background for readability
                    self.screen.blit(name_text, name_background_rect.topleft)

                    pygame.draw.rect(self.screen, (255, 255, 255), dialogue_rect)
                    wrapped_text = self.wrap_text(dialogue, self.dialogue_font, dialogue_rect.width)
                    self.draw_text(wrapped_text, self.dialogue_font, (0, 0, 0), self.screen, dialogue_rect.x + 10, dialogue_rect.y + 10)

    def handle_event(self, event):
        step = self.current_dialogue[self.dialogue_index]
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        pass
                    else:
                        self.sound_played = False
                        if self.choices:
                            self.make_choice()
                        elif self.dialogue_index < len(self.current_dialogue) - 1:
                            self.dialogue_index += 1
                            self.update_choices()
                        else:
                            self.active = False  # End the dialogue sequence
                elif event.key == pygame.K_UP and isinstance(step, dict) and 'choices' in step:
                    self.selected_choice = (self.selected_choice - 1) % len(self.choices)
                elif event.key == pygame.K_DOWN and isinstance(step, dict) and 'choices' in step:
                    self.selected_choice = (self.selected_choice + 1) % len(self.choices)

    def make_choice(self):
        chosen_option = self.choices[self.selected_choice]
        next_step = chosen_option['next']
        self.trigger_dialogue(next_step)  # Continue with the next part of the dialogue

        # Check if the chosen option has an associated event to trigger
        if 'event' in chosen_option:
            self.triggered_event = chosen_option['event']
    
    def reset_triggered_event(self):
        self.triggered_event = None

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        wrapped_lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word + " "
        wrapped_lines.append(current_line)
        return wrapped_lines

    def draw_text(self, text, font, color, surface, x, y):
        for line in text:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (x, y))
            y += font.get_linesize()
    
    def update_choices(self):
        # Get the current dialogue step
        step = self.current_dialogue[self.dialogue_index]

        # Check if the current step is a dictionary and has 'choices'
        if isinstance(step, dict) and 'choices' in step:
            self.choices = step['choices']
        else:
            self.choices = None  # No choices available in this step





def scale_image(img, target_width):
    """ Scale image to target width while maintaining aspect ratio. """
    width, height = img.get_size()
    scaling_factor = target_width / width
    new_height = int(height * scaling_factor)
    return pygame.transform.scale(img, (target_width, new_height))

def scale_player(img, target_width):
    """ Scale image to target width while maintaining aspect ratio. """
    width, height = img.get_size()
    scaling_factor = target_width / width
    new_height = int((height * scaling_factor))
    return pygame.transform.scale(img, (target_width, new_height))

def adapt_scale(img):
    global h, w
    base_img_width = img.get_width()
    scale_ratio = w / 1920
    new_width = int(base_img_width * scale_ratio)
    return scale_image(img, new_width)

def adapt_player_scale(img):
    global h, w
    base_img_width = img.get_width()
    scale_ratio = w / 1920
    new_width = int((base_img_width * scale_ratio)/1.5)
    return scale_player(img, new_width)


pygame.init()
pygame.mixer.init()

player_name = "Jeanne"

#initialisation des images
père_droite = adapt_scale(pygame.image.load('./assets/personnages/pere_droite.png').convert_alpha())
père_gauche = adapt_scale(pygame.image.load('./assets/personnages/pere_gauche.png').convert_alpha())
père_couteau = adapt_scale(pygame.image.load('./assets/personnages/pere_couteau.png').convert_alpha())
mère = adapt_scale(pygame.image.load('./assets/personnages/mere.png').convert_alpha())
player = adapt_scale(pygame.image.load('./assets/personnages/fille.png').convert_alpha())
detective = adapt_scale(pygame.image.load('./assets/personnages/detective.png').convert_alpha())
Truand_1 = adapt_scale(pygame.image.load('./assets/personnages/Truand_1.png').convert_alpha())
Truand_2 = adapt_scale(pygame.image.load('./assets/personnages/Truand_2.png').convert_alpha())
papy = adapt_scale(pygame.image.load('./assets/personnages/Papy.png').convert_alpha())
mamie = adapt_scale(pygame.image.load('./assets/personnages/Mamie.png').convert_alpha())
s_chien = adapt_scale(pygame.image.load('./assets/personnages/chien.png').convert_alpha())
peluche = adapt_scale(pygame.image.load('./assets/personnages/peluche.png').convert_alpha())
player_pistolet = adapt_scale(pygame.image.load('./assets/personnages/fille_pistolet.png').convert_alpha())
player_wp = adapt_scale(pygame.image.load('./assets/personnages/fille_wp.png').convert_alpha())
vide = pygame.image.load('./assets/personnages/vide.png').convert_alpha()
quentin = adapt_scale(pygame.image.load('./assets/personnages/Quentin_the_cailloud.png').convert_alpha())
ivan = adapt_scale(pygame.image.load('./assets/personnages/Ivan_the_cailloud.png').convert_alpha())
zero_two = adapt_scale(pygame.image.load('./assets/personnages/persod.png').convert_alpha())

print("images initialisées")

# Initialize the Dialogue system
dialogue_system = Dialogue(SCREEN, "./assets/Helvetica.ttf", 24)
# Setup dialogues
'''dialogue_system.add_dialogue("clée de dialogue", [
    #un seul personnage
    [("nom",image, "texte", #position sur l'ecran : 'left', 'center', 'right' , True)],#si un seul personnage parle
    #plusieurs personnages affichés en meme temps
    [("nom2",image, "", "center", False), #ne parle pas
    ("nom3",image, "", "right", False), #ne parle pas
    ("nom",image, "texte", "left", True)],#parle
    {'choices': [
        {'text': "text on the button", 'next': "name of the dialogue to go"},
        {'text': "==", 'next': "=="},
        {'text': "==", 'next': "=="}
    ]}
    ])
'''

#intro=================================================================================================================
dialogue_system.add_dialogue("intro", [
    [("Maman", mère, "", "right", False),
     ("Papa", père_gauche, "Où étais-tu passée, espèce de bonne à rien ?!", "left", True)
     ],
    [("Papa", père_gauche, "", "left", False),
     ("Maman", mère, "Je t'en prie, arrête... Je ne sais pas de quoi tu parles... Je...", "right", True)
     ],
    [("Maman", mère, "", "right", False),
     ("Papa", père_gauche, "Tu oses me mentir ?! Tu crois que je suis stupide ?!", "left", True)
     ],
    [("Moi", player, "*Les cris de maman résonnent dans ma tête comme des éclairs de douleur. Je ne peux plus supporter de voir papa la frapper ainsi. Ça me déchire à chaque fois...*", "center", True)
    ],
    [("Maman", mère, "", "right", False),
     ("Papa", père_gauche, "Tu vas regretter de m'avoir menti, salope !", "left", True)
     ],
    [("Moi", player, "*Mon cœur bat la chamade, ma respiration est saccadée. Je ne peux plus rester ici, à regarder maman souffrir. Chaque cri est un coup de poignard pour moi aussi.*", "center", True)
     ],
    [("Papa", père_gauche, "", "left", False),
     ("Maman", mère, "Arrête, s'il te plaît... Je t'en supplie... Ça suffit...", "right", True)
     ],
    [("Maman", mère, "", "right", False),
     ("Papa", père_gauche, "Tais-toi ! Tu ne mérites même pas de parler !", "left", True)
    ],
    [("Moi", player, "*Je dois partir, maintenant. Je ne peux plus supporter cela. Maman ne méritait pas ça, et moi non plus. Je dois trouver un endroit où je serais en sécurité, rester ici signifierais finir comme elle. Battue à mort injustement par un ivrogne dépourvu de coeur...*", "center", True)
     ],
    [("Moi", player, "*Peut-être dehors, je pourrais respirer, penser, fuir tout ça...*", "center", True)
     ],
    [("Papa", père_gauche, f"Reviens ici immédiatement ! {player_name} !", "center", True),
     ],
    [("Moi", player, "*Non, je ne veux pas revenir en arrière. Pas cette fois.*", "center", True)
     ]
    ])

#détective=============================================================================================================
dialogue_system.add_dialogue("detective avec pistolet",[
    [("Inconnu",detective, "Bonsoir, jeune dame. J'aimerais parler avec toi un instant, si tu le permets. Ton père est à ta recherche.", "center", True)],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Je ne veux rien savoir de lui. Pourquoi m'enverrait-il quelqu'un si tout ce qu'il sait faire c'est hurler et blesser ?", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Je comprends ta réticence, vraiment. Mais je ne suis pas là pour discuter  ou même réfléchir à la moralité et à la portée de mes actions de mes actions, vois-tu comme toi je ne cherche qu’à survivre. Enfin bref, ton père veut te récupérer et moi je veux être payé.", "right", True)
    ],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Tu penses sérieusement que je vais accepter de venir avec toi, de retourner auprès de lui après ce qu’il a fait à maman ?", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "J’en suis sûr, qu’importe ce qu’il ait fait, il reste ton père et il peut te protéger, tu penses que ce monde, que ces rues sont mieux que lui. Tout est pareil, partout où tu vas la violence, la haine et la peine sont présentes. Ton père peut t’offrir un toit sur la tête et même a manger dans ton assiette, alors si tu veux survivre tu ferais mieux de m’écouter. De toute façon tu finiras bien par y retourner de gré ou de force.", "right", True)
    ],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Jamais je n’y retournerais, je préférerais mourir plutôt que de retourner vivre avec lui, une vie à ses côté est pire que la mort. Je l’ai compris grâce à maman.", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Tu as plus peur de ton père que de la mort ? C’est compréhensible cependant ce n’est pas le cas de tout le monde et tu dois vivre, parce que la vie est don que ta mère t’as fait, ne gâche pas ça, si tu ne veux pas vivre pour toi, vis pour elle.", "right", True)
    ],
    {'choices': [
        {'text': "Fuir", 'next': "fuir detective", 'event': "fuite_det"},
        {'text': "Rentrer", 'next': "rentrer_det", 'event': "Fin_5"},
        {'text': "Donner la peluche", 'next': "don peluche", 'event' : "doudou"},
        {'text': "L'attaquer", 'next': "tuer det", 'event' : "pistolet"}
    ]}
    ])

dialogue_system.add_dialogue("Rentrer_Maison", [
    [("Moi", player, "C'est ma maison", "center", True)],
    [("Moi", player, "Je ne sais pas si je fais bien d'y retourner mais bon le monde est plus froid que chez moi", "center", True)],
    {'choices': [
        {'text': "Rentrer à la maison", 'next': "rentrer", 'event': "Fin_5"},
        {'text': "Refuser de rentrer et continuer notre errance", 'next': "pas_rentrer"},
    ]}
])

dialogue_system.add_dialogue("rentrer", [
    [("Papa", père_droite, "", "right", False),
    ("Moi", player, "C'est moi papa je suis rentré", "left", True)],
    [("Moi", player, "", "left", False),
     ("Papa", père_droite, "Ah, ça y est tu as fini avec tes conneries ?", "right", True)],
     [("Moi", player, "", "left", False),
     ("Papa", père_droite, "Attrapes une pelle et rejoins moi dans le jardin, on va enterrer ta mère.", "right", True)],
])

dialogue_system.add_dialogue("pas_rentrer", [
    [("Moi", player, "Je ne me sens plus chez moi ici, je n'ai plus rien à y faire", "center", True)]
])


dialogue_system.add_dialogue("detective sans pistolet",[
    [("Inconnu",detective, "Bonsoir, jeune dame. J'aimerais parler avec toi un instant, si tu le permets. Ton père est à ta recherche.", "center", True)],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Je ne veux rien savoir de lui. Pourquoi m'enverrait-il quelqu'un si tout ce qu'il sait faire c'est hurler et blesser ?", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Je comprends ta réticence, vraiment. Mais je ne suis pas là pour discuter  ou même réfléchir à la moralité et à la portée de mes actions de mes actions, vois-tu comme toi je ne cherche qu’à survivre. Enfin bref, ton père veut te récupérer et moi je veux être payé.", "right", True)
    ],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Tu penses sérieusement que je vais accepter de venir avec toi, de retourner auprès de lui après ce qu’il a fait à maman ?", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "J’en suis sûr, qu’importe ce qu’il ait fait, il reste ton père et il peut te protéger, tu penses que ce monde, que ces rues sont mieux que lui. Tout est pareil, partout où tu vas la violence, la haine et la peine sont présentes. Ton père peut t’offrir un toit sur la tête et même a manger dans ton assiette, alors si tu veux survivre tu ferais mieux de m’écouter. De toute façon tu finiras bien par y retourner de gré ou de force.", "right", True)
    ],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Jamais je n’y retournerais, je préférerais mourir plutôt que de retourner vivre avec lui, une vie à ses côté est pire que la mort. Je l’ai compris grâce à maman.", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Tu as plus peur de ton père que de la mort ? C’est compréhensible cependant ce n’est pas le cas de tout le monde et tu dois vivre, parce que la vie est don que ta mère t’as fait, ne gâche pas ça, si tu ne veux pas vivre pour toi, vis pour elle.", "right", True)
    ],
    {'choices': [
        {'text': "Fuir", 'next': "fuir detective", 'event': "fuite_det"},
        {'text': "Rentrer", 'next': "rentrer_det", 'event': "Fin_5"},
        {'text': "Donner la peluche", 'next': "don peluche", 'event' : "doudou"}
    ]}
    ])

dialogue_system.add_dialogue("fuir detective",[
    [("Détective",detective, "", "right", False),
    ("Moi",player, "*Non, je ne peux pas retourner en arrière, pas après tout ce qui s’est passé.*", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Attend petite ! Reviens là, tu ne peux pas survivre seule dehors !..", "right", True)
    ]
])

dialogue_system.add_dialogue("rentrer_det",[
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Disons que je décide de vous faire confiance, que se passera-t-il ? Je rentre, et ensuite ?", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Eh bien c’est une sage décision tu n’as plus qu’à me suivre et je te ramène chez toi.", "right", True)
    ]
])

dialogue_system.add_dialogue("don peluche",[
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Vous voulez vraiment m’aider ? Montrez-lui ça et dites-lui que vous m'avez trouvée et que je suis morte.", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Je... Je peux essayer. Mais Jeanne, ton père pourrait vouloir voir ton corps.", "right", True)
    ],
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Vous n’avez qu’à vous débrouillez avec ça. Je ne compte pas retourner là-bas, alors soit vous faites ça, soit vous me tuez sur le champ et vous amenez mon cadavre à mon père mais je ne crois pas que ce soit pour cela qu’il vous paye.", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Bien je vais essayer. Sois prudente pour la suite.", "right", True)
    ]
])

dialogue_system.add_dialogue("tuer det",[
    [("Détective",detective, "", "right", False),
    ("Moi",player, "Laisse moi tranquille !", "left", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "Attend petite qu'est ce que tu fais ?! Attend ne fais pas ç...", "right", True)
    ],
    [("Moi", player, "", "left", False),
     ("Détective", detective, "", "right", False)
    ]
])

#Pistolet===========================================================================================================
dialogue_system.add_dialogue("Le player trouve le pistolet", [
    [("Moi", player, "La nuit avait enveloppé la ville de son manteau sombre, mais même dans l'obscurité, la violence et la mort semblaient rôder dans chaque coin de rue. Je marchais d'un pas déterminé, mes sens en alerte, mes pensées comme des lames aiguisées dans mon esprit.", "center", True)],
    [("Moi", player, "Mon instinct me disait de fuir, de ne pas m'approcher de cette scène sinistre. Mais la curiosité et un soupçon de cynisme m'incitaient à avancer, à découvrir ce qui se cachait dans l'obscurité.", "center", True)],
    [("Moi", player, "Un pistolet. Comme si la ville n'était pas déjà assez remplie de violence et de mort. Je pourrais presque entendre le rire amer de l'ironie alors que je contemplais cette scène macabre.", "center", True)],
    [("Moi", player, "Mais peut-être que ce pistolet pourrait être utile. Peut-être que dans ce monde impitoyable, je serais plus en sécurité avec une arme entre mes mains qu'avec la simple innocence d'une enfant perdue dans les ténèbres.", "center", True)],
    {'choices': [
        {'text': "Prendre le pistolet", 'next': "prendre", 'event': "take_pistolet"},
        {'text': "Refuser de prendre le pistolet", 'next': "pas_prendre", 'event': "pistoletsuppr"},
        {'text': "Se suicider", 'next': "suicide", 'event': "Fin_2"}
    ]}
])

dialogue_system.add_dialogue("suicide", [
    [("Moi", player, "Plus rien ne m’attend dans cette vie, il ne reste que la misère, la souffrance et la peine. Plus jamais je ne serais capable de sourire, je ne rêve plus du bonheur, je ne rêve plus que de la tranquillité. L’espoir à laissé place à une abîme, à un monstre qui me ronge et me blesse de l’intérieur. Il n’y a plus qu’un solution, attends moi maman j’arrive.", "center", True)],
])

dialogue_system.add_dialogue("pas_prendre", [
    [("Moi", player, "Non. Je ne vais pas tomber dans cette spirale de violence. Je refuse de devenir comme eux. Céder à la violence reviendrait à légitimer les actes et le comportement de mon père.", "center", True)],
    [("Moi", player, "Non, je ne peux pas. Ce n'est pas la solution. Je ne veux pas devenir une part de cette obscurité.", "center", True)],
    [("Moi", player, "Je trouverai un moyen. Je ne vais pas céder à la peur et à la violence. Je suis plus forte que ça.", "center", True)]
])



dialogue_system.add_dialogue("prendre", [
    [("Moi", player, "Il n’y a qu’avec ça que je pourrais garantir ma sécurité, mon père est horrible mais il est à l’image du monde dans lequel nous vivons. Si je veux vivre je dois être forte, plus que la violence. Cette arme me donneras la force de défier la mort et la peur.", "center", True)],
])

#Truands avec pistolet___________________________________________________________________________________________________________________
dialogue_system.add_dialogue("Rencontre avec les truands(pistolet)",[
    [("Truand 1", Truand_1, "", "right", False),
     ("Truand 2", Truand_2, "", "center", False),
     ("Moi", player, "...", "left", True)],
    {'choices': [
        {'text': "Ignorer", 'next': "Inaction agression", 'event': "Truands"},
        {'text': "Tirer", 'next': "Tir sur truand"},
        {'text': "Intervenir diplomatiquement", 'next': "Intervention diplomatique"}
    ]}
])
#Si le player n'interviens pas
dialogue_system.add_dialogue("Inaction agression",[
    [("Moi", player, "Ce que je vois est terrifiant... mais intervenir pourrait me coûter la vie. Parfois, survivre signifie ignorer les horreurs devant nous. Je dois penser à ma sécurité avant tout.", "center", True)]
])
#Si le player tir
dialogue_system.add_dialogue("Tir sur truand",[
    [("Truand 1", Truand_1, "", "right", False),
     ("Truand 2", Truand_2, "", "center", False),
    ("Moi", player, "Laissez-le partir !", "left", True)],
    {'choices': [
        {'text': "Menacer l'autre truand", 'next': "Menace Truand", 'event': "Fin_3"},
        {'text': "Fuir", 'next': "Fuite après tir", 'event': "Truands"}
    ]}
])
#si le joueur menace l'autre truand
dialogue_system.add_dialogue("Menace Truand",[
    [("Truand 1", Truand_1, "", "right", False),
    ("Moi", player, "Ne bouge pas !", "left", True)],
    [("Moi", player, "", "center", False),
     ("Truand 1", Truand_1, "Tu crois vraiment que tu peux nous arrêter avec ça ?", "right", True)],
     [("Moi", player, "", "center", False),
     ("Truand 1", Truand_1, "Tu vas payer pour ce que tu as fait, aucune souffrance, aucun effort ne pourront réparer ce que tu as fait ", "right", True)]
])#Lancer la fin_3

#Si le joueur s'enfuit après avoir tiré
dialogue_system.add_dialogue("Fuite après tir",[
    [("Moi", player, "Je dois m'échapper tant que je le peux encore !", "center", True)]
])

#Si le joueur choisit la voie diplomatique
dialogue_system.add_dialogue("Intervention diplomatique",[
    [("Truand 1", Truand_1, "", "right", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Moi", player, "Arrêtez ça ! Vous n'avez pas besoin de faire du mal à quelqu'un pour prouver votre force. ", "left", True)],
    [("Moi", player, "", "left", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Truand 1", Truand_1, "T’en as dans le froc pour nous interrompre", "right", True)],
    [("Moi", player, "", "left", False),
    ("Truand 1", Truand_1, "", "right", False),
    ("Truand 2", Truand_2, "Tu a l’air de fuir quelque chose, faisons un deal : Tu dépouille et tu frappe ce morveux puis tu pourras nous rejoindre.", "center", True)],
    [("Moi", player, "", "left", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Truand 1", Truand_1, "On te promet pas la richesse ni le bonheur, mais avec nous tu seras en sécurité et tu ne manqueras de rien tant que tu nous aideras. Ici-bas le bonheur est un luxe que peu de gens peuvent s’offrir, mais la sécurité, ça c’est un question de groupe et de nombre. Rejoins nous et tu n’auras plus jamais peur.", "right", True)],
    {'choices': [
        {'text': "Partir", 'next': "Partir", 'event': "Truands"},
        {'text': "Faire ce qu'ils demandent", 'next': "agression enfant", 'event': "Fin_6"},
        {'text': "La diplomatie a échoué, place au sang", 'next': "Tir sur truand"}
    ]}
])
#Si le Joueur Part
dialogue_system.add_dialogue("Partir",[
    [("Moi", player, "Rien de bon ne sortira de ce marché. Je ferais mieux de partir.", "center", True)]
])
#Si le joueur agresse l'enfant
dialogue_system.add_dialogue("agression enfant",[
    [("Truand 1", Truand_1, "", "right", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Moi", player, "il faut que j’accepte, tout vaut mieux que de retourner vivre avec papa. Ils ont raison, la sécurité à un prix et je ne veux plus errer sans but et dans la peur de la mort à chaque croisement.", "left", True)],
    [("Truand 1", Truand_1, "", "right", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Moi", player, "Très bien j’accepte", "left", True)],
    [("Moi", player, "", "left", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Truand 1", Truand_1, "Bienvenue dans la bande. Tu es des nôtres maintenant. ", "right", True)],
])
#Truands sans pistolet___________________________________________________________________________________________________________________
dialogue_system.add_dialogue("Rencontre avec les truands(sans pistolet)",[
    [("Truand 1", Truand_1, "", "right", False),
     ("Truand 2", Truand_2, "", "center", False),
     ("Moi", player, "...", "left", True)],
    {'choices': [
        {'text': "Ignorer", 'next': "Inaction agression", 'event': "Truands"},
        {'text': "Intervenir diplomatiquement", 'next': "Intervention diplomatique (sans pistolet)" }
    ]}
])

dialogue_system.add_dialogue("Intervention diplomatique (sans pistolet)",[
    [("Truand 1", Truand_1, "", "right", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Moi", player, "Arrêtez ça ! Vous n'avez pas besoin de faire du mal à quelqu'un pour prouver votre force. ", "left", True)],
    [("Moi", player, "", "left", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Truand 1", Truand_1, "T’en as dans le froc pour nous interrompre", "right", True)],
    [("Moi", player, "", "left", False),
    ("Truand 1", Truand_1, "", "right", False),
    ("Truand 2", Truand_2, "Tu a l’air de fuir quelque chose, faisons un deal : Tu dépouille et tu frappe ce morveux puis tu pourras nous rejoindre.", "center", True)],
    [("Moi", player, "", "left", False),
    ("Truand 2", Truand_2, "", "center", False),
    ("Truand 1", Truand_1, "On te promet pas la richesse ni le bonheur, mais avec nous tu seras en sécurité et tu ne manqueras de rien tant que tu nous aideras. Ici-bas le bonheur est un luxe que peu de gens peuvent s’offrir, mais la sécurité, ça c’est un question de groupe et de nombre. Rejoins nous et tu n’auras plus jamais peur.", "right", True)],
    {'choices': [
        {'text': "Partir", 'next': "Partir", 'event': "Truands"},
        {'text': "Faire ce qu'ils demandent", 'next': "agression enfant", 'event': "Fin_6"},
    ]}
])

#les vieux_______________________________________________________________________________________________________________________
dialogue_system.add_dialogue("Rencontre avec les vieux (bon)",[
    [("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "", "center", False),
    ("Moi", player, "...", "left", True)],
    {'choices': [
        {'text': "Demander de l'aide", 'next': "dialogue vieux", 'event': "Fin_4"},
        {'text': "Ne rien faire", 'next': "Inaction vieux", 'event': "vieux"},
    ]}
])

dialogue_system.add_dialogue("dialogue vieux",[
    [("Moi", player, "", "left", False),
    ("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "Oh, ma petite, mais que t’est-il arrivé ? Tu es blessée ! Hugues nous devons l’aider.", "center", True),
    ],
    [("Moi", player, "", "left", False),
    ("Vieille", mamie, "", "center", False),
    ("Vieux", papy, "Et ton jouet est tout abîmé... Viens ici, voyons ce que nous pouvons faire pour toi.", "right", True),
    ],
    [("Moi", player, "", "left", False),
    ("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "Qu'est-ce qui t'a amenée ici toute seule, chérie ? Tu as de la famille chez qui on pourrait t’amener ?", "center", True),
    ],
    [("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "", "center", False),
    ("Moi", player, "J'en avait une", "left", True)
    ],
    [("Moi", player, "", "left", False),
    ("Vieille", mamie, "", "center", False),
    ("Vieux", papy, "Tu es en sécurité avec nous maintenant. Ne t’inquiète pas.", "right", True),
    ],
    [("Moi", player, "", "left", False),
    ("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "Voilà, ton ami est presque comme neuf. Que dirais-tu de venir chez nous, on pourrait t’aider, tu pourras te rétablir puis on décideras quoi faire ensuite?", "center", True),
    ]
])

dialogue_system.add_dialogue("Inaction vieux",[
    [("Moi", player, "ça ne sers à rien, personne ne peu m'aider et tout le monde m'ignore", "left", True)],
])

dialogue_system.add_dialogue("Rencontre avec les vieux (pas bon)",[
    [("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "", "center", False),
    ("Moi", player, "...", "left", True)],
    {'choices': [
        {'text': "Demander de l'aide", 'next': "dialogue vieux pas bon", 'event': "vieux"},
        {'text': "Ne rien faire", 'next': "Inaction vieux", 'event': "vieux"},
    ]}
])

dialogue_system.add_dialogue("dialogue vieux pas bon",[
    [("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "", "center", False),
    ("Moi", player, "Bonjour... Puis-je...", "left", True)
    ],
    [("Moi", player, "", "left", False),
    ("Vieux", papy, "", "right", False),
    ("Vieille", mamie, "Nous ne pouvons rien pour toi, jeune fille. C’est triste de voir tant de jeunes dans la rue ces jours-ci.", "center", True),
    ],
    [("Moi", player, "", "left", False),
    ("Vieille", mamie, "", "center", False),
    ("Vieux", papy, "Que veux-tu c'est comme ça maintenant et puis ce n'est pas comme si on pouvait guérir la misère", "right", True),
    ],
    [("Moi", player, "Ils m'ont ignoré", "center", True)],
])

#le chien______________________________________________________________________________________________________________________________________
dialogue_system.add_dialogue("Rencontre avec chien (avec pistolet)",[
    [("Moi", player, "Qu'est-ce que...?.", "center", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "C'est bon, chien... je ne vais pas te faire de mal.", "left", True)],
    [("Moi", player, "", "left", False),
    ("Chien", s_chien, "Grrrrrrrh", "right", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Non ! Arrête ça !", "left", True)],
    [("Moi", player, "", "left", False),
    ("Chien", s_chien, "Grrrrrrrh ouaf ouaf grrrrrrrrrrh", "right", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Aïe ! Lâche ça, s'il te plaît !", "left", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Oh non, pas ça... pourquoi ?", "left", True)],
    {'choices': [
        {'text': "Partir", 'next': "Partir chien", 'event': "blessée"},
        {'text': "Abattre le démon", 'next': "Tir sur chien", 'event': "pistochien"},
    ]}
])
#Si on tire:
dialogue_system.add_dialogue("Tir sur chien",[
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Crève, crève, crève !!", "left", True)],
    [("Moi", player, "... Il est  temps de se remettre en route", "center", True)],
])
#Si on part:
dialogue_system.add_dialogue("Partir chien",[
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Vite il faut que je parte", "left", True)],
])

#Chien sans pistolet
dialogue_system.add_dialogue("Rencontre avec chien (sans pistolet)",[
    [("Moi", player, "Qu'est-ce que...?.", "center", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "C'est bon, chien... je ne vais pas te faire de mal.", "left", True)],
    [("Moi", player, "", "left", False),
    ("Chien", s_chien, "Grrrrrrrh", "right", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Non ! Arrête ça !", "left", True)],
    [("Moi", player, "", "left", False),
    ("Chien", s_chien, "Grrrrrrrh ouaf ouaf grrrrrrrrrrh", "right", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Aïe ! Lâche ça, s'il te plaît !", "left", True)],
    [("Chien", s_chien, "", "right", False),
    ("Moi", player, "Oh non, pas ça... pourquoi ?", "left", True)],
    {'choices': [
        {'text': "Partir", 'next': "Partir chien", 'event': "blessée"},
    ]}
])

#le père================================================================================================================
dialogue_system.add_dialogue("papa pistolet",[
    [("Papa",père_droite, f"Enfin, je t'ai trouvée. Il est temps de rentrer à la maison, {player_name}.", "center", True)
    ],
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "Papa, je... je ne peux pas revenir. Pas après tout ce qui s'est passé.", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "Tu penses que là dehors tu es chez toi, tu penses toucher la liberté. Laisse moi te dire une chose, la liberté ce n’est qu’un mot, un idéal bon pour les naïfs, combien de cadavres as-tu vu, combien de personne s’en prennent aux autres. Est-ce ça la liberté à laquelle tu aspires. Cesse tes enfantillages et retournons à la maison. Il n’y a pas d’autre endroit où tu seras acceptée, tu n’as pas d’autre endroit où te réfugier. Si tu refuses tu te condamne à mort et ta mère n’aurais pas voulu ça, elle ne voudrait pas que tu la rejoignes.", "right", True)
    ],
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "Que sais-tu de ce que voulait maman ? A part les blessures que tu lui causé tu ne sais rien d’elle ?", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "La seule chose que je sais d’elle, c’est qu’elle t’aimais et qu’elle est libre aujourd’hui, viens avec moi, je suis le seul souvenir que tu ais d’elle. ", "right", True)
    ],
    {'choices': [
        {'text': "Fuir", 'next': "fuir papa avec pistolet"},
        {'text': "Rentrer", 'next': "rentrer_pap", 'event': "Fin_5"}
    ]}
    ])

dialogue_system.add_dialogue("papa sans pistolet",[
    [("Papa",père_droite, f"Enfin, je t'ai trouvée. Il est temps de rentrer à la maison, {player_name}.", "center", True)
    ],
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "Papa, je... je ne peux pas revenir. Pas après tout ce qui s'est passé.", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "Tu penses que là dehors tu es chez toi, tu penses toucher la liberté. Laisse moi te dire une chose, la liberté ce n’est qu’un mot, un idéal bon pour les naïfs, combien de cadavres as-tu vu, combien de personne s’en prennent aux autres. Est-ce ça la liberté à laquelle tu aspires. Cesse tes enfantillages et retournons à la maison. Il n’y a pas d’autre endroit où tu seras acceptée, tu n’as pas d’autre endroit où te réfugier. Si tu refuses tu te condamne à mort et ta mère n’aurais pas voulu ça, elle ne voudrait pas que tu la rejoignes.", "right", True)
    ],
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "Que sais-tu de ce que voulait maman ? A part les blessures que tu lui causé tu ne sais rien d’elle ?", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "La seule chose que je sais d’elle, c’est qu’elle t’aimais et qu’elle est libre aujourd’hui, viens avec moi, je suis le seul souvenir que tu ais d’elle. ", "right", True)
    ],
    {'choices': [
        {'text': "Fuir", 'next': "fuir papa sans pistolet"},
        {'text': "Rentrer", 'next': "rentrer_pap", 'event': "Fin_5"}
    ]}
    ])

dialogue_system.add_dialogue("rentrer_pap",[
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "*Je ne peux survivre seule dehors, ça me fait mal mais j’ai besoin d’aide et puis je n’ai pas le choix si je ne veux pas mourir maintenant, si c’est pas lui, le monde se chargera de me tuer. Je dois vivre pour elle.*", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "Bon tu te magnes ?", "right", True)
    ],
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "*J’arrive...", "center", True)
    ]
])

dialogue_system.add_dialogue("fuir papa avec pistolet",[
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "Non, je ne peux pas faire ça. Je ne peux plus vivre avec toi.", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "Tu n'as pas le choix !", "center", True)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Moi",player_wp, "", "left", False),
     ("Papa",père_couteau, "", "center", False)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Moi",player_wp, "", "left", False), 
     ("Papa",père_couteau, "Si tu ne viens pas de ton plein gré, je devrai prendre des mesures drastiques. Tu ne veux pas que je fasse du mal à ton seul ami, n'est-ce pas ?", "center", True)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Papa",père_couteau, "", "center", False),
     ("Moi",player_wp, "Ne lui fais pas de mal, je t'en supplie...", "left", True)
    ],
    {'choices': [
        {'text': "Tuer", 'next': "tuer papa", 'event': "tuer_pap"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"}
    ]}
])

dialogue_system.add_dialogue("fuir papa sans pistolet",[
    [("Papa",père_droite, "", "right", False),
    ("Moi",player, "Non, je ne peux pas faire ça. Je ne peux plus vivre avec toi.", "left", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "Tu n'as pas le choix !", "center", True)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Moi",player_wp, "", "left", False),
     ("Papa",père_couteau, "", "center", False)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Moi",player_wp, "", "left", False),
     ("Papa",père_couteau, "Si tu ne viens pas de ton plein gré, je devrai prendre des mesures drastiques. Tu ne veux pas que je fasse du mal à ton seul ami, n'est-ce pas ?", "center", True)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Papa",père_couteau, "", "center", False),
     ("Moi",player_wp, "Ne lui fais pas de mal, je t'en supplie...", "left", True)
    ],
    {'choices': [
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"},
        {'text': "Rentrer", 'next': "rentrer_pap2", 'event': "Fin_5"}
    ]}
])

dialogue_system.add_dialogue("tuer papa",[
    [("Doudou",peluche, "", "center_left", False),
     ("Papa",père_couteau, "", "center", False),
     ("Moi",player_pistolet, "Non, ça suffit. Ça s'arrête maintenant !", "left", True)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Moi",player_pistolet, "", "left", False)
    ],
    [("Moi",player, "C'est fini... Je suis libre maintenant, maintenant maman est vengé, j’espère qu’elle est en paix en sachant que papa ne pourras plus faire de mal.", "left", True)
    ],
])

dialogue_system.add_dialogue("rentrer_pap2",[
    [("Doudou",peluche, "", "center_left", False),
     ("Papa",père_couteau, "", "center", False),
     ("Moi",player_wp, "D'accord, arrête ! Je vais rentrer avec toi. Ne lui fais pas de mal...", "left", True)
    ],
    [("Doudou",peluche, "", "center_left", False),
     ("Moi",player_wp, "", "left", False),
     ("Papa",père_droite, "Sage décision. Allons-y.", "center", True)
    ],
    [("Moi",player, "", "left", False),
     ("Papa",père_droite, "", "center", False)
    ]
])

#________________________________FIN_________________________________________________________________
#Fin_1
dialogue_system.add_dialogue("Fin_1",[
    [("", vide, "Jeanne, après avoir longtemps fui les dangers et les douleurs de sa vie passée, se trouve égarée dans les dédales interminables des rues sombres de la ville. Chaque pas est un combat contre la fatigue qui s'empare de son corps, chaque souffle un rappel de ses peurs et de son isolement. La ville, avec ses lumières vacillantes et ses ombres menaçantes, semble se refermer sur elle, un labyrinthe sans fin qui l'érode lentement.", "center", True)],
    [("", vide, "Sans but et sans espoir, elle erre sans destination, son esprit submergé par la tristesse et l'épuisement. La solitude pèse lourdement sur ses épaules, chaque coin de rue lui rappelant ce qu'elle a fui et ce qu'elle a perdu. Les bruits de la ville, autrefois un murmure constant, deviennent un vacarme assourdissant qui résonne dans son crâne fatigué.", "center", True)],
    [("", vide, "Au fur et à mesure que les heures s'étirent, la force de Jeanne s'amenuise. Sa démarche devient chancelante, ses yeux lourds de sommeil et de désespoir. Elle réalise qu'elle ne peut plus continuer, son corps refusant d'obéir à sa volonté de survivre. Un banc abandonné sur le trottoir lui offre un répit temporaire, et sans penser à autre chose qu'à son besoin impérieux de repos, elle s'y affaisse.", "center", True)],
    [("", vide, "Le froid du métal sous elle est presque un soulagement, et elle s'y allonge, son souffle devenant superficiel. Les lumières de la ville flottent au-dessus d'elle comme des étoiles lointaines, indifférentes à son sort. Dans cet instant de solitude absolue, Jeanne sent les derniers fils de son énergie se dissiper.", "center", True)],
    [("", vide, "Ses paupières se ferment lentement, son esprit s'échappant vers des souvenirs de jours meilleurs, des échos de rires et de chaleur humaine. Mais même ces souvenirs s'estompent rapidement, remplacés par le noir silencieux de l'inconscience. C'est dans ce noir complet, seul et non observé, que Jeanne trouve une paix étrange, son cœur battant son dernier rythme, sa respiration s'évanouissant dans l'air froid de la nuit.", "center", True)],
    [("", vide, "Elle ne se réveillera pas. Son corps reste immobile sur le banc, une figure solitaire perdue dans l'immensité de la ville. Le monde continue de tourner autour d'elle, indifférent et incessant, alors que Jeanne s'éteint doucement, un autre visage oublié dans les marges sombres de la ville.", "center", True)],
])


#Fin_3
dialogue_system.add_dialogue("Fin_3",[
    [("", vide, "Dans un crescendo brutal de violence et de revanche, la vie de Jeanne bascule irrémédiablement après avoir pris la décision fatale de tirer sur l'un des truands. Les conséquences de son acte la rattrapent plus vite qu'elle ne l'aurait imaginé. La nuit même, les complices du truand tombé lui tendent une embuscade, mue par un désir de vengeance qui ne connaît aucune pitié.", "center", True)],
    [("", vide, "Traquée dans les ruelles sombres qu'elle avait appris à naviguer, Jeanne se retrouve rapidement acculée, la peur palpable dans ses yeux alors qu'elle fait face à ses assaillants. Ils sont impitoyables, leurs visages marqués par la colère et la résolution de rendre justice selon leur propre loi brutale.", "center", True)],
    [("", vide, "Tu as pris l'un des nôtres, fille, gronde le chef du gang, une lueur cruelle dans les yeux. Maintenant, tu vas payer le prix ultime.", "center", True)],
    [("", vide, "Les mains de Jeanne sont liées derrière son dos avec une brutalité désinvolte, et avant qu'elle puisse protester ou plaider pour sa vie, un nœud coulant est passé autour de son cou. Elle est poussée sous le cadre d'une porte de service, où une poutre dépasse assez pour servir de gibet improvisé. La corde est attachée avec une efficacité morose, chaque mouvement des truands étant calculé et froid.", "center", True)],
    [("", vide, "La gravité de sa situation atteint un sommet terrifiant alors que Jeanne se retrouve pendue par le cou, ses pieds battant désespérément l'air dans une lutte futile pour la survie. Le monde commence à tourner autour d'elle, ses pensées s'embrouillant dans la panique et l'incrédulité de sa fin imminente.", "center", True)],
    [("", vide, "Les derniers moments de Jeanne sont empreints d'une horreur vertigineuse, ses yeux capturant les visages distordus de ses bourreaux pour la dernière fois. Le bruit étouffé de ses propres halètements se mêle au murmure sinistre du vent nocturne, tandis que les lumières de la ville clignotent au loin, indifférentes à la tragédie qui se déroule dans leur ombre.", "center", True)],
    [("", vide, "Sa lutte s'achève lentement, son corps se balançant doucement dans la brise nocturne, une silhouette sombre et solitaire contre le ciel urbain. Les truands disparaissent dans les ténèbres, laissant derrière eux le corps de Jeanne comme un sombre avertissement aux étoiles impassibles au-dessus.", "center", True)],
    [("", vide, "Ainsi se termine la vie de Jeanne, non pas comme un murmure, mais comme un cri silencieux dans la nuit; un rappel brutal que dans certaines histoires, les choix que l'on fait peuvent conduire à des fins tragiques et irrévocables, suspendus entre les mailles sombres de la justice et de la vengeance.", "center", True)]

])


#Fin_5
dialogue_system.add_dialogue("Fin_5",[
    [("", vide, "Contrainte par les circonstances et épuisée par ses errances, Jeanne retourne finalement à la maison paternelle, un lieu qui résonne avec le silence pesant de l'absence de sa mère. Dès le seuil franchi, un sentiment de résignation l'envahit ; elle sait que les jours à venir seront remplis de la présence oppressive de son père, dont les excuses et les promesses n'ont jamais tenu leurs garanties.", "center", True)],
    [("", vide, "Les jours se succèdent, tous plus semblables les uns que les autres. Son père, sous le vernis d'une façade réformée, maintient un contrôle strict, masquant mal ses anciennes tendances sous des règles rigides et des attentes irréalistes. Jeanne se retrouve piégée dans une routine étouffante, où chaque geste semble surveillé et chaque parole pesée pour éviter les conflits.", "center", True)],
    [("", vide, "À la table du dîner, les conversations sont superficielles, souvent interrompues par le spectre de ce qui s’est passé. Jeanne mange en silence, répondant par monosyllabes, tandis que son père tente de rapiécer ce qui ne peut être réparé. La maison, bien que propre et ordonnée, est dénuée de chaleur, chaque pièce résonnant du fantôme des cris et des pleurs de sa mère.", "center", True)],
    [("", vide, "Parfois, dans la solitude de sa chambre, Jeanne permet à ses pensées de vagabonder vers des 'et si'. Et si elle avait fait un choix différent ? Et si elle avait trouvé la force de s'échapper pour de bon ? Ces pensées la hantent, mais la fatigue et le désespoir la ramènent toujours à la dure réalité de sa situation.", "center", True)],
    [("", vide, "Avec le temps, une certaine acceptation s'installe. Jeanne apprend à naviguer dans les eaux troubles de ce nouvel équilibre familial, trouvant de petits moments de paix dans des plaisirs solitaires : la lecture, les promenades tardives dans le jardin, quand la présence de son père se fait moins oppressante. Elle s'efforce de reconstruire sa vie morceau par morceau, mais le poids de la perte et du regret ne la quitte jamais complètement.", "center", True)],
    [("", vide, "Cette vie, choisie sous la contrainte, devient son nouveau normal. Jeanne survit, mais à quel prix ? La liberté, un rêve lointain, flotte toujours à l'horizon, un rappel douloureux de ce qui aurait pu être si les cartes avaient été distribuées différemment. Pour l'instant, elle endure, une survivante dans une maison qui ressemble plus à une prison qu'à un foyer.", "center", True)],
])

#Fin_2
dialogue_system.add_dialogue("Fin_2",[
    [("", vide, "La solitude et le désespoir avaient longtemps été les compagnons constants de Jeanne dans son pèlerinage à travers les rues sans fin de la ville. Dans un acte presque mécanique, elle ramasse un pistolet abandonné, un vestige lugubre d'une violence omniprésente qui imprègne chaque coin de rue de sa sombre présence. Son regard se pose sur l'objet métallique, un reflet brillant de sa propre perte d'espoir et de direction.", 'center', True)],
    [("", vide, "Avec une gravité accablante, Jeanne s'isole dans une ruelle déserte, à l'écart des yeux indiscrets et des oreilles qui pourraient intercepter son dernier acte de solitude. Elle pense à sa mère, à son père, à toutes les décisions qui l'ont menée ici, à ce point de non-retour. Le pistolet, froid et impersonnel dans sa main tremblante, semble être le seul objet qui comprend son désespoir, le seul qui peut offrir une échappatoire à son agonie incessante.", 'center', True)],
    [("", vide, "Les pensées de Jeanne se bousculent, chaotiques et rapides, alors qu'elle lutte avec l'idée de mettre fin à ses souffrances. Chaque souvenir, chaque moment de joie passée lui paraît à la fois distant et douloureux, une cruelle moquerie de ce que sa vie aurait pu être.", 'center', True)],
    [("", vide, "Les rires partagés, les larmes versées, tout cela ne semble plus avoir de place dans le monde froid et indifférent qui l'entoure.", 'center', True)],
    [("", vide, "Finalement, avec une résignation sombre, elle place le canon du pistolet contre sa tempe. Son souffle se fait saccadé, et un silence oppressant enveloppe la scène. Un moment suspendu dans le temps, un dernier souffle, et puis le bruit sec et définitif du coup de feu rompt le silence.", 'center', True)],
    [("", vide, "La chute de Jeanne est douce, presque comme un soupir, son corps s'effondrant contre le sol froid et impitoyable de la ruelle. Le pistolet glisse de sa main inerte, une déclaration silencieuse de sa dernière décision. L'écho du coup de feu se dissipe rapidement, laissant derrière lui un vide immédiat, une absence de vie là où Jeanne avait un jour lutté, aimé et rêvé.", 'center', True)],
    [("", vide, "Dans les jours qui suivent, la ville continue son rythme incessant, indifférente au destin d'une âme de plus perdue dans ses profondeurs. Mais pour ceux qui avaient connu et aimé Jeanne, ce coup de feu résonne comme un rappel sombre de la fragilité de la vie et de la cruauté du désespoir qui peut consumer même les esprits les plus lumineux. Son histoire se termine dans cette ruelle sombre, une tragédie personnelle dans la vaste tapisserie de la ville, un rappel poignant que parfois, la douleur devient trop lourde pour être portée seule.", 'center', True)]
])

#Fin_4
dialogue_system.add_dialogue("Fin_4",[
    [("", vide, "Après une longue et éprouvante errance dans les rues sombres et indifférentes de la ville, Jeanne trouve refuge auprès d'un couple de personnes âgées qui la découvrent, blessée et seule, sur un banc public. Avec une gentillesse qui semble rare dans son monde, ils l'accueillent chez eux, loin de l'atmosphère toxique de son foyer familial.", 'center', True)],
    [("", vide, "Dans cette nouvelle maison, chaque jour apporte un souffle de chaleur humaine que Jeanne croyait perdu à jamais. Le couple, sans enfants eux-mêmes, comble le vide de leur quotidien en offrant à Jeanne l'affection et le soutien dont elle a été privée. Ils l'écoutent sans jugement, la consolent dans ses moments de doute, et la guident avec une sagesse douce et patiente.", 'center', True)],
    [("", vide, "La vieille dame, avec ses yeux pétillants et ses mains habiles, enseigne à Jeanne l'art de la broderie et du jardinage, transformant leur petite cour en un havre de paix verdoyant. Le vieil homme, quant à lui, partage avec elle son amour pour les livres et les échecs, remplissant leurs soirées de discussions enrichissantes et de parties stratégiques qui stimulent l'esprit de la jeune fille.", 'center', True)],
    [("", vide, "Peu à peu, les cicatrices internes de Jeanne commencent à guérir. Elle rit plus souvent, ses cauchemars se font moins fréquents, et elle trouve dans la routine rassurante de cette maison une stabilité longtemps désirée. Le couple l'intègre comme leur propre fille, et elle, en retour, s'épanouit sous leur affection inconditionnelle. La maison résonne des échos de leur vie quotidienne, chaque repas partagé, chaque anniversaire célébré ensemble renforçant les liens qui les unissent.", 'center', True)],
    [("", vide, "L'amour et le respect mutuel qu'ils partagent redonnent à Jeanne la force de se projeter dans l'avenir avec espoir. Elle commence même à envisager des études, rêvant de devenir enseignante ou travailleuse sociale, inspirée par la bienveillance du couple qui l'a sauvée.", 'center', True)],
    [("", vide, "En trouvant ce nouveau foyer, Jeanne découvre qu'il est possible de reconstruire sa vie, de trouver un sens à sa souffrance, et de regarder vers l'avenir non pas avec crainte, mais avec l'anticipation joyeuse de tout ce qui reste à découvrir et à aimer. Leur maison, autrefois silencieuse, est maintenant remplie de la musique de leur existence commune, un symbole vivant que même dans les plus grandes ténèbres, il y a une lumière qui attend d'être trouvée, si seulement on a le courage de continuer à chercher.", 'center', True)]
])

#Fin_6
dialogue_system.add_dialogue("Fin_6",[
    [("", vide, "Après avoir échappé de justesse à la vie oppressante sous le toit paternel, Jeanne trouve une étrange acceptation parmi les ombres de la ville : une bande de truands qui, comme elle, ont été rejetés ou brisés par la société. Chaque jour est un défi, une vie au bord du gouffre, où la loi du plus fort règne en maître.", 'center', True)],
    [("", vide, "Initialement, Jeanne ressent une bouffée de liberté ; ici, il n'y a pas de jugements hypocrites, seulement la survie brute. Elle apprend rapidement les ficelles du métier : l'art de l'intimidation, le maniement des armes, et les subtilités de la furtivité. Ses nouveaux « amis » l'introduisent dans un monde sans règles, où chaque membre porte ses cicatrices comme des badges d'honneur.", 'center', True)],
    [("", vide, "Avec le temps, cependant, la réalité de sa décision commence à peser sur elle. Les actions du groupe, souvent cruelles et impitoyables, la forcent à s'interroger sur sa propre nature. A-t-elle vraiment échappé à l'oppression, ou a-t-elle simplement échangé une cage pour une autre, plus dangereuse et imprévisible ?", 'center', True)],
    [("", vide, "Les nuits où elle trouve le sommeil, Jeanne rêve de routes non prises, mais au réveil, les rues sombres de la ville lui rappellent que sa place est désormais parmi ceux qui, comme elle, n'ont nulle part où aller. Ironiquement, dans ce monde de ténèbres, elle trouve une sorte de fraternité tordue. Elle est respectée, crainte, et parfois même aimée, mais au fond, le doute persiste.", 'center', True)],
    [("", vide, "Est-ce vraiment mieux que de vivre sous l'ombre oppressante de son père ? Peut-être pas, mais pour Jeanne, c'est un choix de survie, un chemin où elle tient les rênes, même si le cheval est lancé à plein galop vers une fin incertaine. C'est sa vie maintenant, et elle la vivra à ses propres termes, pour le meilleur ou pour le pire.", 'center', True)]
])

dialogue_system.add_dialogue("Egg",[
    [("Quentin", quentin, "", "left", False), 
     ("002", zero_two, "", "center", False), 
     ("Ivan", ivan, "Oh... Mais qui voilà ?", "right", True)],
    [("Ivan", ivan, "", "right", False),
     ("002", zero_two, "", "center", False),
    ("Quentin", quentin, "On dirait bien que notre création a envie de parcourir du chemin", "left", True)],
    [("Ivan", ivan, "", "right", False),
    ("Quentin", quentin, "", "left", False),
    ("002", zero_two, "Ou alors elle est indécise concernant ce qu'elle doit faire, le chemin qu'elle doit prendre", "center", True)],
    {'choices': [
        {'text': "Fuir", 'next': "fuite_entités", 'event': "Fin_1"},
        {'text': "Tirer", 'next': "tir_entités", 'event': "Fin_1"},
        {'text': "Répondre", 'next': "répondre_entités", 'event': "Fin_1"}
    ]}
])

dialogue_system.add_dialogue("fuite_entités",[
    [("Quentin", quentin, "", "center", False), 
     ("Ivan", ivan, "", "right", False), 
     ("Moi", player, "Laissez moi !!!!!", "left", True)],
    [("Ivan", ivan, "", "right", False), 
    ("Moi", player, "", "left", False),
    ("Quentin", quentin, "ça ne sert à rien, dès que tu nous a vu, c'est la fin", "center", True)],
    [("Quentin", quentin, "", "center", False), 
     ("Moi", player, "", "left", False), 
     ("Ivan", ivan, "Tu es bien  trop fatigué pour aller quelque part, le mieux c'est que tu te repose", "right", True)],
    [("Ivan", ivan, "", "right", False), 
     ("Moi", player, "", "left", False),
     ("002", zero_two, "Nous sommes seulemnt des hallucinations causés par ta trop longue errance", "center", True)]
])

dialogue_system.add_dialogue("tir_entités",[
    [("Quentin", quentin, "", "center", False), 
     ("Ivan", ivan, "", "right", False), 
     ("Moi", player_pistolet, "Laissez moi, je ne suis la création de personne", "left", True)],
    [("Ivan", ivan, "", "right", False), 
    ("Moi", player_pistolet, "", "left", False),
    ("Quentin", quentin, "ça ne sert à rien, nous ne sommes pas à proprement parler des corps physiques", "center", True)],
    [("Quentin", quentin, "", "center", False), 
     ("Moi", player_pistolet, "", "left", False), 
     ("Ivan", ivan, "Pour faire simple nous sommes là tout en y étant pas", "right", True)],
    [("Ivan", ivan, "", "right", False), 
     ("Moi", player_pistolet, "", "left", False),
     ("002", zero_two, "Disons que nous sommes à la fois des divinité et des êtres qui ne sont présents que parce que ton cerveau est épuisé et qu'un paradoxe spatial et temporel s'est formé depuis ton esprit à la suite de ta longue errance.", "center", True)],
    [("002", zero_two, "", "right", False), 
     ("Moi", player_pistolet, "", "left", False), 
     ("Ivan", ivan, "Maintenant endors-toi.", "center", True)],
])

dialogue_system.add_dialogue("répondre_entités",[
    [("Quentin", quentin, "", "center", False), 
     ("Ivan", ivan, "", "right", False), 
     ("Moi", player, "Qui êtes vous !?", "left", True)],
    [("Ivan", ivan, "", "right", False), 
    ("Moi", player, "", "left", False),
    ("Quentin", quentin, "La représentation materielle de tes pensées sur le plan quantique...", "center", True)],
    [("Quentin", quentin, "", "center", False), 
     ("Moi", player, "", "left", False), 
     ("Ivan", ivan, "...incarnés par les anges démons et commandés par nul autre que ton esprit. En termes plus simples, des dieux.", "right", True)],
    [("Ivan", ivan, "", "right", False), 
     ("Moi", player, "", "left", False),
     ("002", zero_two, f"Nous ne pouvons pas te laisser vivre ainsi, ton érrance a deja été bien assez longue... Au revoir {player_name}.", "center", True)]
])


current_dialogue_key = "intro"
dialogue_triggered = False