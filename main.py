import pygame
import sys
import json
import os
from pygame.locals import KEYDOWN, K_RETURN
from model.player import Player
from model.player2 import Player2
from settings import LARGURA, ALTURA, LARGURA_MUND0, ALTURA_MUNDO
if os.path.exists("dados/vitorias.json"):
      with open("dados/vitorias.json","r") as arq:
         vitorias=json.load(arq)
else:
    vitorias=[]
vitorias=[]
pygame.init()
fonte = pygame.font.SysFont("arial", 36)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("f1 do piteco")
bg = pygame.image.load("imagens/pista.jpg").convert()
bg = pygame.transform.scale(bg, (LARGURA_MUND0, ALTURA_MUNDO))
player = Player(100, 100)
player2 = Player2(100, 200)
all_sprites = pygame.sprite.Group()
all_sprites.add(player, player2)

clock = pygame.time.Clock()
mensagem = ""
partidas = 0
rodando = True
tempo=pygame.time.get_ticks()
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            pygame.quit()
            sys.exit()
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player2.update(pressed_keys)
    tempo_game=pygame.time.get_ticks()
    tempo_prova=(tempo_game-tempo)//1000
    camera_x = min(0, max(LARGURA - LARGURA_MUND0, -player.rect.centerx + LARGURA // 2))
    camera_y = min(0, max(ALTURA - ALTURA_MUNDO, -player.rect.centery + ALTURA // 2))
    tela.blit(bg, (camera_x, camera_y))

    for entity in all_sprites:
        tela.blit(entity.surf, (entity.rect.x + camera_x, entity.rect.y + camera_y))
    if player.venceu() and mensagem == "":
        mensagem = f"player 1 win!{tempo_prova} seconds"
        partidas += 1
        jogo={"resultado":"vitoria player 1","partida":partidas,"tempo em segundos":tempo_prova }
        vitorias.append(jogo)
        with open("dados/vitorias.json","w") as arq:
            json.dump(vitorias,arq,indent=4)
    elif player2.venceu() and mensagem == "":
        mensagem = f"player 2 win!{tempo_prova} seconds"
        partidas += 1
        jogo={"resultado":"vitoria player 2","partida":partidas,"tempo em segundos":tempo_prova}
        vitorias.append(jogo)
        with open("dados/vitorias.json","w") as arq:
            json.dump(vitorias,arq,indent=4)
    if partidas > 0:
        if event.type == KEYDOWN and event.key == K_RETURN:
            player.resetar_partida()
            player2.resetar_partida()
            tempo=pygame.time.get_ticks()
            mensagem = ""
        texto = fonte.render(mensagem, True, (0, 0, 0))
        tela.blit(texto, (100, 100))

    pygame.display.flip()
    clock.tick(60)
