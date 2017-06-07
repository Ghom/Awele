import pygame
from pygame.locals import *

class BackSprite(pygame.sprite.Sprite):
        def __init__(self, window, group=None):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.Surface(window.get_size()).convert()
            self.image.fill((255,255,255))
            self.rect = self.image.get_rect()
            
class Sprite(pygame.sprite.Sprite):
        def __init__(self, counter, group=None):
            
            pygame.sprite.Sprite.__init__(self, group)
            self.counter = counter
            self.counter_prev = 0
            
            self.image = pygame.Surface((100,100)).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, (255,0,0), [ (0,0), (100,100) ], 1)
            self.rect = self.image.get_rect()
            
            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.counter)
            label = myfont.render(text, 1, (255,0,0))
            self.image.blit(label, self.rect.center)

        def update(self):
            #return
            if(counter != self.counter_prev):
                print(counter)
                self.counter_prev = counter
            
            self.image = pygame.Surface((100,100)).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, (255,0,0), [ (0,0), (100,100) ], 1)
            self.rect = self.image.get_rect()

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.counter)
            self.image = label = myfont.render(text, 1, (255,0,0))
            self.image.blit(label, self.rect.center)


Quit = False
counter = 0

pygame.init()
pygame.display.set_icon( pygame.Surface((0,0)) )
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption( 'test' )

render_back = pygame.sprite.RenderUpdates()
render = pygame.sprite.RenderUpdates()
back = BackSprite(window, render_back)
back.rect = (0,0)

render_back.draw(window)
pygame.display.flip()

sprite = Sprite(counter, render)
render.draw( window )
pygame.display.flip()
  
while not Quit:
    for event in pygame.event.get():    
        if event.type == QUIT:
            Quit = True
        if event.type == KEYDOWN:
            counter += 1

    window.fill( (255,255,255) )

    render[0].update()

    window.blit( sprite.image, sprite.rect )
    #dirty1 = render_back.draw(window)
    #dirty2 = render.draw(window)
    #pygame.display.update( dirty1 + dirty2 )

    pygame.display.update()

    
#end while
    
pygame.quit()
    
