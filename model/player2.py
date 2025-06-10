import pygame
import random
from pygame.locals import RLEACCEL
from settings import LARGURA_MUND0,ALTURA_MUNDO,ALTURA,LARGURA

class Player2(pygame.sprite.Sprite):
          def __init__(self,x,y):
                  super (Player2,self).__init__()
                  self.surf=pygame.image.load("imagens/car.png").convert_alpha()
                  self.surf=pygame.transform.scale(self.surf,(70,60))
                  self.surf.set_colorkey((255,255,255),RLEACCEL)
                  self.rect=self.surf.get_rect()
                  self.rect.x = x
                  self.rect.y = y
                  self.start_pos=(self.rect.x,self.rect.y)
          def update(self, pressed_keys):
                  self.speed = random.randint(4,5)
                  if pressed_keys[pygame.K_e]:
                       self.rect.y-=self.speed
                  if pressed_keys[pygame.K_x]:
                      self.rect.y==self.speed
                  if pressed_keys[pygame.K_d]:
                         self.rect.x+=self.speed
                         
                  if pressed_keys[pygame.K_s]:
                         self.rect.x-=self.speed 
                  if pressed_keys[pygame.K_f] :
                         self.rect.x+=self.speed                     

                  if self.rect.left>LARGURA_MUND0:
                         self.rect.left=LARGURA_MUND0
                  if self.rect.top<=0:
                         self.rect.top=0
                  if self.rect.bottom>=ALTURA_MUNDO:
                         self.rect.bottom=ALTURA_MUNDO
              
          def desenhar(self,tela,cam_x,cam_y):
                 global pos_x,pos_y
                 pos_x=self.rect.x-cam_x
                 pos_y=self.rect.y-cam_y

                 tela.blit(tela,(pos_x,pos_y,70,60))

          def resetar_partida(self):
                   self.rect.topleft=self.start_pos
          def venceu(self):
                   return self.rect.right>LARGURA_MUND0

          
                 
              
            
       