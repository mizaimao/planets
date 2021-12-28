
import pygame
import os


PROJECT_NAME = "Chicken Space Game"
VERSION = '0.0.1'
# main settings
FPS = 60
WIDTH, HEIGHT = 800, 600

# init
pygame.font.init()
pygame.mixer.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(PROJECT_NAME + " v" + VERSION)
WIN.fill((100,100,100))


def draw_window(color: tuple):
    WIN.fill(color)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

if __name__ == '__main__':
    main()
