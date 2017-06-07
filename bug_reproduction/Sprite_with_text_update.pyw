import pygame
from pygame.locals import *
            
class Sprite(pygame.sprite.Sprite):
        def __init__(self, group=None):
            
            pygame.sprite.Sprite.__init__(self, group)
            self.counter = 0
            
            self.image = pygame.Surface((100,100)).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, (255,0,0), [ (0,0), (100,100) ], 1)
            self.rect = self.image.get_rect()
            
            self.myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.counter)
            label = self.myfont.render(text, 1, (255,0,0))
            self.image.blit(label, self.rect.center)

        def update(self):
            rect_save = self.rect
            self.image = pygame.Surface((100,100)).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, (255,0,0), [ (0,0), (100,100) ], 1)
            self.rect = self.image.get_rect()
            self.rect.x = rect_save[0]
            self.rect.y = rect_save[1]
            
            text = str(self.counter)
            label = self.myfont.render(text, 1, (255,0,0))
                    
            self.image.blit(label, self.rect.center)


Quit = False

pygame.init()
window = pygame.display.set_mode((640, 480))
render = pygame.sprite.RenderUpdates()

sprite = Sprite(render)
BUG = False
if BUG:
    sprite.rect = (300,300)

  
while not Quit:
    for event in pygame.event.get():    
        if event.type == QUIT:
            Quit = True
        if event.type == KEYDOWN:
            sprite.counter += 1
    
    background = pygame.Surface( window.get_size() )
    background.fill( (0,0,0) )
    render.clear( window, background )

    render.update()

    dirty = render.draw(window)
    pygame.display.update( dirty )
#end while
    
pygame.quit()
    
