import  sys
import  pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_setting, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False

def check_events(ai_setting,stats ,screen, aliens,ship, bullets,play_button,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_setting, screen, ship, bullets)


        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mourse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting,screen,play_button,ship,aliens,stats,bullets,mouse_x,mourse_y,sb)


def update_buttlets(ai_setting,screen,ship,aliens,bullets,stats,sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting,screen,ship,aliens,bullets,stats,sb)



def update_screen(ai_settings, screen, ship,bullets,aliens,stats ,play_button,sb):
    screen.fill(ai_settings.bg_color)
    for buttet in bullets.sprites():
        buttet.draw_buttet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def get_number_alients_x(ai_setting, alien_width):
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def creat_alient(ai_setting, screen, aliens,alien_number,raw_number):
    alient = Alien(ai_setting, screen)
    alien_width = alient.rect.width
    alient.x = alien_width + 2 * alien_width * alien_number
    alient.rect.x = alient.x
    alient.rect.y = alient.rect.height + 2 * alient.rect.height * raw_number
    aliens.add(alient)

def creat_fleet(ai_setting,screen,aliens,ship):
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_alients_x(ai_setting,alien.rect.width)
    number_raws = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)

    for row_number in range(number_raws):
        for alien_number in range(number_aliens_x):
            creat_alient(ai_setting, screen, aliens,alien_number,row_number)

def get_number_rows(ai_setting, ship_height, alient_height):
    avilable_apace_y = (ai_setting.screen_height - 3 *  alient_height - ship_height)
    number_raw = int(avilable_apace_y / (2 * alient_height))
    return number_raw

def update_alients(ai_setting, screen,ship, alients,stats,bullets,sb):
    check_fleet_edges(ai_setting,alients)
    alients.update()
    if pygame.sprite.spritecollideany(ship, alients):
        ship_hit(ai_setting, screen, ship, alients, stats, bullets,sb)
    check_alients_bottom(ai_setting, screen, ship, alients, stats, bullets,sb)


def check_fleet_edges(ai_setting,alients):
    for alient in alients.sprites():
        if alient.check_edages():
            change_fleet_direction(ai_setting, alients)
            break

def change_fleet_direction(ai_setting,alients):
    for alient in alients.sprites():
        alient.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1

def check_bullet_alien_collisions(ai_setting,screen,ship,aliens,bullets,stats,sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for ailents in collisions.values():
            stats.score += ai_setting.alient_score * len(ailents)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()

        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_setting, screen, aliens, ship)

def ship_hit(ai_setting,screen, ship, alients , stats,bullets,sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        alients.empty()
        bullets.empty()
        creat_fleet(ai_setting,screen,alients,ship)
        ship.center_ship()
        sleep(0.5)
    else :
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alients_bottom(ai_setting,screen, ship, alients , stats,bullets,sb):
    screent_rect = screen.get_rect()
    for alien in alients.sprites():
        if alien.rect.bottom >= screent_rect.bottom:
            ship_hit(ai_setting, screen, ship, alients, stats, bullets,sb)
            break


def check_play_button(ai_setting,screen,play_button,ship,alients,stats,bullets,mouse_x,mourse_y,sb):
    button_clicked = play_button.rect.collidepoint(mouse_x,mourse_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynameic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        stats.reset_stats()
        alients.empty()
        bullets.empty()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        creat_fleet(ai_setting,screen,alients,ship)
        ship.center_ship()

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()