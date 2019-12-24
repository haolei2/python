import pygame
import sys
from setting import Setting
from ship import  Ship
import  game_functions as gf
from pygame.sprite import  Group
from alien import  Alien
from game_stats import  GameStatus
from button import  Button
from scoreboard import  Scoreboard

def run_game():
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption(ai_setting.name)
    ship = Ship(ai_setting, screen)
    bullets = Group()
    aliens = Group()
    gf.creat_fleet(ai_setting,screen,aliens,ship)
    stats = GameStatus(ai_setting)
    play_button = Button(ai_setting,screen,"Play")
    sb = Scoreboard(ai_setting,stats ,screen)

    while True:
        gf.check_events(ai_setting,stats ,screen, aliens,ship, bullets,play_button,sb)

        if stats.game_active:
            ship.update()
            gf.update_buttlets(ai_setting,screen,ship,aliens,bullets,stats,sb)
            gf.update_alients(ai_setting,screen,ship,aliens,stats,bullets,sb)

        gf.update_screen(ai_setting, screen, ship, bullets,aliens, stats ,play_button,sb)



run_game()
