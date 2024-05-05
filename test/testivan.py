import pygame

class Dialogue:
    def __init__(self, screen, font_path, font_size=32, background_opacity=128):
        self.screen = screen
        self.dialogue_font = pygame.font.Font(font_path, font_size)
        self.name_font = pygame.font.Font(font_path, font_size)
        self.dialogues = {}
        self.current_dialogue = None
        self.dialogue_index = 0
        self.background_opacity = background_opacity
        self.active = False

    def add_dialogue(self, key, dialogues):
        # dialogues should be a list of tuples (character_name, portrait, dialogue_text)
        self.dialogues[key] = dialogues

    def trigger_dialogue(self, key):
        if key in self.dialogues:
            self.current_dialogue = self.dialogues[key]
            self.dialogue_index = 0
            self.active = True

    def draw(self):
        if not self.active or not self.current_dialogue:
            return
        
        character_name, portrait, dialogue = self.current_dialogue[self.dialogue_index]
        
        # Background with opacity
        background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        background.set_alpha(self.background_opacity)
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        
        # Calculate positions and dimensions
        portrait_rect = portrait.get_rect(topleft=(50, 50))
        dialogue_rect = pygame.Rect(50, self.screen.get_height() - 150, self.screen.get_width() - 100, 100)
        name_rect = pygame.Rect(50, self.screen.get_height() - 200, self.screen.get_width() - 100, 50)
        
        # Draw portrait
        self.screen.blit(portrait, portrait_rect)
        
        # Draw dialogue box
        pygame.draw.rect(self.screen, (255, 255, 255), dialogue_rect)
        wrapped_text = self.wrap_text(dialogue, self.dialogue_font, dialogue_rect.width)
        self.draw_text(wrapped_text, self.dialogue_font, (0, 0, 0), self.screen, dialogue_rect.x + 10, dialogue_rect.y + 10)
        
        # Draw name
        name_surface = self.name_font.render(character_name, True, (0, 0, 0))
        self.screen.blit(name_surface, (name_rect.x + 10, name_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.dialogue_index < len(self.current_dialogue) - 1:
                self.dialogue_index += 1
            else:
                self.active = False  # End the dialogue sequence

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


# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)

# Initialize the Dialogue system
dialogue_system = Dialogue(screen, "./assets/Helvetica.ttf", 24)

# Load character portraits
zerotwo = pygame.image.load('./assets/perso.png').convert_alpha()
quentin = pygame.image.load('./assets/photo_de_classe_de_moi.jpg').convert_alpha()

# Setup dialogues
dialogue_system.add_dialogue("dialogue1", [
    ("Zero Two", zerotwo, "Salut darling Quentin, t'as bien dormis ? j'ai revé de toi cette nuit et je me suis reveillée... toute mouillée..."),
    ("Zero Two", zerotwo, "Peut-être que tu veux plus de détails sur ce qu'il se passait ?")
])
dialogue_system.add_dialogue("dialogue2", [
    ("Quentin GigaChad", quentin, "Oh non sans façon je préfère me Gogo Gadget à l'inspecteur sur Stellaris.")
])

# Use a variable to control which dialogue is currently being shown
current_dialogue_key = "dialogue1"
dialogue_triggered = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        dialogue_system.handle_event(event)

    # Only trigger a dialogue once based on some condition
    if not dialogue_triggered:
        dialogue_system.trigger_dialogue(current_dialogue_key)
        dialogue_triggered = True

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the dialogue
    dialogue_system.draw()

    # Update the display
    pygame.display.flip()
    
    # Check if the dialogue has finished to possibly trigger the next one
    if not dialogue_system.active:
        if current_dialogue_key == "dialogue1":
            current_dialogue_key = "dialogue2"
            dialogue_triggered = False
        elif current_dialogue_key == "dialogue2":
            # No more dialogues, do something or end the game loop
            break

pygame.quit()
