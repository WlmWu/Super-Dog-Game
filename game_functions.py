import sys
import pygame
from game_status import GameState

def check_events(server, stats, button = None, player = None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button(server, stats, button, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, player)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)

def check_button(server, status, button, mouse_x, mouse_y):
    if button is None:
        return
    if button.rect.collidepoint(mouse_x, mouse_y):
        if status.state == GameState.NOTSTART:
            pygame.mouse.set_visible(False)
            status.reset_status()
            status.game_start()
        elif status.state == GameState.END:
            pygame.mouse.set_visible(False)
            server.reset()
            status.reset_status()
            status.game_start()
        
def check_keydown_events(event, player):
    if player is None:
        return
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    elif event.key == pygame.K_UP:
        player.moving_up = True
    elif event.key == pygame.K_DOWN:
        player.moving_down = True
    # elif event.key == pygame.K_SPACE:
        # dog.jump()
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, player):
    if player is None:
        return
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False
    elif event.key == pygame.K_UP:
        player.moving_up = False
    elif event.key == pygame.K_DOWN:
        player.moving_down = False

def checkGetPoint(player, item, scoreboard, status):
    if pygame.sprite.collide_rect(player, item):
        scoreboard.score += item.point
        item.update(status, False)
        if item.point < 0:
            player.behurted()

def checkItemsCollide(items, status):
    itemsCenter = [(i.rect.centery, i) for i in items]
    itemsCenter.sort(key = lambda t: t[0])
    for i in range(1, len(itemsCenter)):
        c1, i1 = itemsCenter[i-1]
        c2, i2 = itemsCenter[i]
        x1, w1 = i1.x, i1.width
        x2, w2 = i2.x, i2.width
        if c1 + w1/2 > c2 - w2/2:
            if x1 < x2:
                i2.reset_pos(status)
            else:
                i1.reset_pos(status)
