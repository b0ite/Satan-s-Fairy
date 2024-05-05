import pygame, time

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (170, 170, 170)

font = pygame.font.Font(None, 32)

#--------------------------------------------------------------------------------
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

#--------------------------------------------------------------------------------

class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, min_value, max_value, name="Slider"):
        super().__init__()
        self.name = name
        self.font = pygame.font.Font(None, 40)
        self.value_font = pygame.font.Font(None, 40)
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        # The initial rects are set here, but their positions and sizes will be updated in update_dimensions
        self.slider_bar_rect = pygame.Rect(x, y, width, height)
        self.handle_width = 20
        self.handle_rect = pygame.Rect(x, y, self.handle_width, height)
        self.dragging = False

    def update_dimensions(self, w, h, relative_x, relative_y, relative_width, relative_height):
        # Update the slider's width and height based on window size
        self.width = w * relative_width
        self.height = h * relative_height
        # Update the slider's position
        new_x = w * relative_x
        new_y = h * relative_y
        # Update the slider bar and handle rects
        self.slider_bar_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        self.handle_rect = pygame.Rect(new_x, new_y, self.handle_width, self.height)

    def draw(self, surface):
        # Draw name
        name_surface = self.font.render(self.name, True, (255, 255, 255))  # White color
        name_rect = name_surface.get_rect(topleft=(self.slider_bar_rect.left - 200, self.slider_bar_rect.centery - 30))
        surface.blit(name_surface, name_rect)
        
        # Draw slider bar
        pygame.draw.rect(surface, (150, 150, 150), self.slider_bar_rect)
        
        # Draw slider handle
        pygame.draw.rect(surface, (100, 100, 100), self.handle_rect)
        
        # Draw value
        value_surface = self.value_font.render(str(round(self.value, 2)), True, (255, 255, 255))  # White color
        value_rect = value_surface.get_rect(center=(self.handle_rect.centerx, self.slider_bar_rect.top - 10))
        surface.blit(value_surface, value_rect)

    def update_value(self):
        # Update the value based on the handle's position
        range_ = self.max_value//1 - self.min_value//1
        relative_pos = (self.handle_rect.centerx - self.slider_bar_rect.left) / self.width
        self.value = (self.min_value//1 + range_ * relative_pos)-2.5

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = min(max(event.pos[0], self.slider_bar_rect.left), self.slider_bar_rect.right - self.handle_width)
                self.handle_rect.x = new_x
                self.update_value()



class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.selected_index = 0
        self.is_open = False
        self.option_height = height  # Height of each dropdown option

    def draw(self, surface):
        # Draw the main box
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.options[self.selected_index], True, BLACK)
        surface.blit(text_surface, (self.x + 5, self.y + 5))
        
        if self.is_open:
            # Draw options
            for i, option in enumerate(self.options):
                pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y + self.height * (i + 1), self.width, self.option_height))
                text_surface = font.render(option, True, BLACK)
                surface.blit(text_surface, (self.x + 5, self.y + self.height * (i + 1) + 5))
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_open:
                # Check if click is on any option
                for i in range(len(self.options)):
                    rect = pygame.Rect(self.x, self.y + self.height * (i + 1), self.width, self.option_height)
                    if rect.collidepoint(event.pos):
                        self.selected_index = i
                        pygame.display.set_mode((int(self.options[i].split('x')[0]), int(self.options[i].split('x')[1])), pygame.RESIZABLE)
                        self.is_open = False
                        break
            else:
                rect = pygame.Rect(self.x, self.y, self.width, self.height)
                if rect.collidepoint(event.pos):
                    self.is_open = not self.is_open


def fade_to_black(screen, duration=1000):
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    steps = range(0, 256, 5)  # Fade in from transparent to opaque
    for alpha in steps:
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)  # Maintain a smooth transition with 60 FPS
        pygame.time.delay(duration // len(steps))  # Evenly distribute the delay over the fade steps

def lower_volume(step=0.1, duration=1000):
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(0, current_volume - step)
    while current_volume > new_volume:
        current_volume -= step
        pygame.mixer.music.set_volume(max(0, current_volume))  # Ensure volume doesn't go negative
        pygame.time.delay(duration // 10)
        print(f"Current Volume: {current_volume}")  # Optional: print current volume

def increase_volume(step=0.1, duration=1000):
    current_volume = pygame.mixer.music.get_volume()
    new_volume = min(1, current_volume + step)
    while current_volume < new_volume:
        current_volume += step
        pygame.mixer.music.set_volume(min(1, current_volume))  # Ensure volume doesn't exceed 1
        pygame.time.delay(duration // 10)
        print(f"Current Volume: {current_volume}")  # Optional: print current volume

