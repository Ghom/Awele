import pygame
from pygame.locals import *

class Sprite(pygame.sprite.Sprite):
        def __init__(self, counter, group=None):
            
            pygame.sprite.Sprite.__init__(self, group)
            self.counter = counter
        
            #self.image = pygame.Surface((100,100)).convert()
            #self.image.fill((0,0,0,0))
            #self.rect = self.image.get_rect()
            
            self.myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.counter)
            self.image = self.myfont.render(text, 1, (255,0,0))
            self.rect = self.image.get_rect()
            #self.image.blit(label, self.rect.center)

        def update(self):
            text = str(self.counter)
            self.image = self.myfont.render(text, 1, (255,0,0))
            #self.image.blit(label, self.rect.center)


pygame.init()
window = pygame.display.set_mode((640, 480))
Quit = False
counter = 0

background = pygame.Surface( window.get_size() )
background.fill( (0,0,0) )

render = pygame.sprite.RenderUpdates()
sprite = Sprite(counter, render)
  
while not Quit:
    for event in pygame.event.get():    
        if event.type == QUIT:
            Quit = True
        if event.type == KEYDOWN:
            counter += 1
    render.clear( window, background )        
    dirty = render.draw(window)
    pygame.display.update( dirty )
#end while
    
pygame.quit()
    
