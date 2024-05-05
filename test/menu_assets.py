import pygame

# Ensure Pygame is initialized
pygame.init()

class Slider:
    def __init__(self, name, val, maxi, mini, pos):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos[0]  # x-location on screen
        self.ypos = pos[1]
        self.surf = pygame.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.font = pygame.font.Font(None, 30)
        self.txt_surf = self.font.render(name, 1, (255, 255, 255))
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, (255, 255, 255), [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, (0, 255, 0), [10, 10, 80, 10], 0)

        # Dynamic graphics - movable slider
        self.slider = pygame.Rect(0, 0, 20, 20)
        self.slider.center = (10+int((val-mini)/(maxi-mini)*80), 25)

    def draw(self, screen):
        """ Draw the slider """
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, (255, 255, 255), [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, (0, 255, 0), [10, 10, 80, 10], 0)
        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface
        self.slider.center = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 25)
        pygame.draw.rect(self.surf, (255, 0, 0), self.slider)

        # move of button box to correct screen position
        self.surf.set_colorkey((0, 0, 0))
        screen.blit(self.surf, (self.xpos, self.ypos))

    def move(self):
        """
        The dynamic part; reacts to movement of the slider button.
        """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi
        self.slider.center = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 25)
