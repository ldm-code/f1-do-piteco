
import pygame
import sys
import json
import os

from pygame.locals import KEYDOWN, K_RETURN

from model.player import Player
from model.player2 import Player2

from settings import (
    LARGURA,
    ALTURA,
    LARGURA_MUND0,
    ALTURA_MUNDO
)


# =====================================
# CARREGAR VITORIAS SALVAS
# =====================================

if os.path.exists("dados/vitorias.json"):

    with open("dados/vitorias.json", "r") as arq:
        vitorias = json.load(arq)

else:
    vitorias = []


# =====================================
# INICIALIZACAO DO PYGAME
# =====================================

pygame.init()

fonte = pygame.font.SysFont("arial", 36)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("F1 do Piteco")

bg = pygame.image.load(
    "imagens/pista.jpg"
).convert()

bg = pygame.transform.scale(
    bg,
    (LARGURA_MUND0, ALTURA_MUNDO)
)


# =====================================
# CRIACAO DOS JOGADORES
# =====================================

player = Player(100, 100)
player2 = Player2(100, 200)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, player2)


# =====================================
# VARIAVEIS DO JOGO
# =====================================

clock = pygame.time.Clock()

rodando = True

mensagem = ""

# Quantidade de partidas nesta execução
partidas = 0

# Controle da contagem regressiva
contagem_iniciada = pygame.time.get_ticks()

corrida_iniciada = False

tempo = 0
tempo_prova = 0


# =====================================
# LOOP PRINCIPAL
# =====================================

while rodando:

    # ---------------------------------
    # EVENTOS
    # ---------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == KEYDOWN:

            # Reiniciar depois de uma vitoria
            if event.key == K_RETURN and mensagem != "":

                player.resetar_partida()
                player2.resetar_partida()

                mensagem = ""

                corrida_iniciada = False

                contagem_iniciada = pygame.time.get_ticks()

                tempo = 0
                tempo_prova = 0


    # ---------------------------------
    # CONTAGEM REGRESSIVA
    # ---------------------------------

    tempo_game = pygame.time.get_ticks()

    tempo_contagem = (
        tempo_game - contagem_iniciada
    ) // 1000

    if not corrida_iniciada and tempo_contagem >= 3:

        corrida_iniciada = True

        # O cronometro comeca agora
        tempo = pygame.time.get_ticks()


    # ---------------------------------
    # MOVIMENTACAO
    # ---------------------------------

    pressed_keys = pygame.key.get_pressed()

    if corrida_iniciada and mensagem == "":

        # Jogador controlado pelo usuario
        player.update(pressed_keys)

        # Jogador 2 controlado pela IA
        player2.update_npc()

        # Tempo da corrida
        tempo_prova = (
            pygame.time.get_ticks() - tempo
        ) // 1000


    # ---------------------------------
    # CAMERA
    # ---------------------------------

    camera_x = min(
        0,
        max(
            LARGURA - LARGURA_MUND0,
            -player.rect.centerx + LARGURA // 2
        )
    )

    camera_y = min(
        0,
        max(
            ALTURA - ALTURA_MUNDO,
            -player.rect.centery + ALTURA // 2
        )
    )


    # ---------------------------------
    # DESENHAR FUNDO
    # ---------------------------------

    tela.blit(bg, (camera_x, camera_y))


    # ---------------------------------
    # DESENHAR JOGADORES
    # ---------------------------------

    for entity in all_sprites:

        tela.blit(
            entity.surf,
            (
                entity.rect.x + camera_x,
                entity.rect.y + camera_y
            )
        )


    # ---------------------------------
    # VERIFICAR VITORIA
    # ---------------------------------

    if corrida_iniciada and mensagem == "":
        if pygame.sprite.collide_rect(player, player2):
                        mensagem = (
                            f"Acidente Com "
                            f"{tempo_prova} segundos"
                        )
            
                        partidas += 1
            
                        jogo = {
                            "resultado": "Acidente",
                            "partida": partidas,
                            "tempo em segundos": tempo_prova
                        }
            
                        vitorias.append(jogo)

        if player.venceu():

            mensagem = (
                f"Player 1 venceu! "
                f"{tempo_prova} segundos"
            )

            partidas += 1

            jogo = {
                "resultado": "vitoria player 1",
                "partida": partidas,
                "tempo em segundos": tempo_prova
            }

            vitorias.append(jogo)

        elif player2.venceu():

            mensagem = (
                f"Player 2 venceu! "
                f"{tempo_prova} segundos"
            )

            partidas += 1

            jogo = {
                "resultado": "vitoria player 2",
                "partida": partidas,
                "tempo em segundos": tempo_prova
            }

            vitorias.append(jogo)

        # Salvar resultado somente quando
        # uma partida terminar
        if mensagem != "":

            with open(
                "dados/vitorias.json", "w"
            ) as arq:

                json.dump(
                    vitorias,
                    arq,
                    indent=4
                )


    # ---------------------------------
    # MOSTRAR CONTAGEM REGRESSIVA
    # ---------------------------------

    if not corrida_iniciada:

        restante = 3 - tempo_contagem

        if restante > 0:

            texto = fonte.render(
                str(restante),
                True,
                (255, 255, 255)
            )

        else:

            texto = fonte.render(
                "VAI!",
                True,
                (0, 255, 0)
            )

        tela.blit(
            texto,
            (
                LARGURA // 2 - texto.get_width() // 2,
                ALTURA // 2 - texto.get_height() // 2
            )
        )


    # ---------------------------------
    # MOSTRAR RESULTADO
    # ---------------------------------

    if mensagem != "":

        texto = fonte.render(
            mensagem,
            True,
            (255, 255, 255)
        )

        tela.blit(texto, (100, 100))

        texto_enter = fonte.render(
            "Pressione ENTER para jogar novamente",
            True,
            (255, 255, 255)
        )

        tela.blit(texto_enter, (100, 150))


    # ---------------------------------
    # ATUALIZAR TELA
    # ---------------------------------

    pygame.display.flip()

    clock.tick(60)


# =====================================
# ENCERRAR
# =====================================

pygame.quit()
sys.exit()