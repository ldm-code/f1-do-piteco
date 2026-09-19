import random
import pygame
from pygame.locals import RLEACCEL
from settings import LARGURA_MUND0, ALTURA_MUNDO


class Player2(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.surf = pygame.image.load(
            "imagens/car.png"
        ).convert_alpha()

        self.surf = pygame.transform.scale(
            self.surf, (70, 60)
        )

        self.surf.set_colorkey(
            (255, 255, 255), RLEACCEL
        )

        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_pos = (x, y)


    def update_npc(self):
        speeds=[11,7,8,10]
        speed=random.choice(speeds)
        # Velocidade do NPC
        self.velocidade = speed

        # O NPC avança automaticamente
        if not self.venceu():
            self.rect.x += self.velocidade

        # Impede que ultrapasse o mapa
        if self.rect.right > LARGURA_MUND0:
            self.rect.right = LARGURA_MUND0

    def update(self, pressed_keys):
        # Mantido para permitir controle manual,
        # caso você queira testar o NPC manualmente.
        pass

    def desenhar(self, tela, cam_x, cam_y):

        tela.blit(
            self.surf,
            (
                self.rect.x + cam_x,
                self.rect.y + cam_y
            )
        )

    def resetar_partida(self):

        self.rect.topleft = self.start_pos

    def venceu(self):

        return self.rect.right >= LARGURA_MUND0