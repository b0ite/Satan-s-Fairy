import pygame
import sys
from needed import slider

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 35)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if slider.slider.collidepoint(event.pos):
                slider.hit = True
        if event.type == pygame.MOUSEBUTTONUP:
            slider.hit = False

    if slider.hit:
        slider.move()

    screen.fill((30, 30, 30))
    slider.draw(screen)
    
    # Display slider value
    value_surf = font.render(f'{int(slider.val)}', True, (255, 255, 255))
    screen.blit(value_surf, (slider.xpos + 50, slider.ypos - 30))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
