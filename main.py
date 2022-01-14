import pygame as p
import neat
import random
import sys
import os

p.init()
screen = p.display.set_mode((480, 700))
import Globals
from Jojo import Jojo
from Аrmature import Armature
from Hammer import Hammer

p.display.set_caption("Swing Jojo")

BLINK_ANIMATION = p.USEREVENT
p.time.set_timer(BLINK_ANIMATION, 100)

FAN_ANIMATION = p.USEREVENT + 1
p.time.set_timer(FAN_ANIMATION, 30)

SPAWN_ARMATURE = p.USEREVENT + 2
p.time.set_timer(SPAWN_ARMATURE, 1250)

clock = p.time.Clock()

is_ground_visible = True
game_Y = 0
play_button_rect = None
back_button_rect = None


def draw_background(screen, y):
    global color, game_Y, is_ground_visible
    buildings = p.transform.smoothscale(Globals.IMAGES['BUILDINGS'],
                                  ((Globals.WIDTH, Globals.HEIGHT * Globals.BUILDINGS_RATIO)))
    ground = p.transform.smoothscale(Globals.IMAGES['GROUND'], (Globals.WIDTH, Globals.HEIGHT * Globals.GROUND_RATIO))
    back_ground = p.transform.smoothscale(Globals.IMAGES['BACKGROUND'][color], (Globals.WIDTH, Globals.HEIGHT))
    clouds = p.transform.smoothscale(Globals.IMAGES['CLOUDS'][color],
                               ((Globals.WIDTH * Globals.CLOUDS_RATIO, Globals.IMAGES['CLOUDS'][color].get_height())))

    screen.blit(back_ground, (0, 0))
    screen.blit(clouds, ((Globals.WIDTH - clouds.get_width()) // 2, y))
    screen.blit(clouds, ((Globals.WIDTH - clouds.get_width()) // 2, y - Globals.HEIGHT))
    screen.blit(clouds, ((Globals.WIDTH - clouds.get_width()) // 2, y + Globals.HEIGHT // 2))
    screen.blit(clouds, ((Globals.WIDTH - clouds.get_width()) // 2, y - Globals.HEIGHT // 2))

    if y < ground.get_height() * 1.5 and is_ground_visible:
        screen.blit(buildings, (0, y + Globals.HEIGHT - buildings.get_height()))
        screen.blit(ground, (0, y + Globals.HEIGHT - ground.get_height()))
    if y >= Globals.HEIGHT:
        is_ground_visible = False
        game_Y = 0


def check_score(curr, jojo, armatures):
    for sprite in armatures.sprites():
        if sprite.rect.y == jojo.rect.y and sprite.dir == -1:  # need dir check to prevent +2 instead +1 score
            curr += 1
    return curr


def int2image(score, option):
    score_digit_list = [int(x) for x in str(score)]
    numbers_sprites = Globals.IMAGES['U_NUMBERS'] if option == 'U' else Globals.IMAGES['L_NUMBERS']
    offset = 2
    space_x = numbers_sprites[0].get_width() * len(score_digit_list) + (len(score_digit_list) - 1) * offset
    space_y = numbers_sprites[0].get_height()
    score_rect = p.Rect((0, 0), (space_x, space_y))
    score_surface = p.Surface((score_rect.width, score_rect.height), p.SRCALPHA, 32)
    for i, number in enumerate(score_digit_list):
        score_surface.blit(numbers_sprites[number], ((numbers_sprites[number].get_width() + offset) * i, 0))
    return score_surface


def draw_game_over(screen, score, score_img, high_score_img):
    text = Globals.IMAGES['GAME_OVER']['TEXT']
    text_rect = text.get_rect(center=(Globals.WIDTH // 2, 150))
    screen.blit(text, text_rect)

    # main panel
    panel = Globals.IMAGES['GAME_OVER']['PANEL']
    panel_rect = panel.get_rect(midtop=(Globals.WIDTH // 2, 225))
    panel_surface = p.Surface((panel_rect.width, panel_rect.height), p.SRCALPHA, 32)
    panel_surface.blit(panel, (0, 0))

    # score
    score_rect = score_img.get_rect(midright=(315, 68))
    panel_surface.blit(score_img, score_rect)

    # hs

    high_score_rect = high_score_img.get_rect(midright=(315, 130))
    panel_surface.blit(high_score_img, high_score_rect)

    if 5 <= score < 10:
        medal_img = Globals.IMAGES['MEDAL']['BRONZE']
    elif 10 <= score < 25:
        medal_img = Globals.IMAGES['MEDAL']['SILVER']
    elif 25 <= score < 50:
        medal_img = Globals.IMAGES['MEDAL']['GOLD']
    elif 50 <= score:
        medal_img = Globals.IMAGES['MEDAL']['PLATINUM']

    if score >= 5:
        medal_rect = medal_img.get_rect(center=(80, 102))
        panel_surface.blit(medal_img, medal_rect)
    screen.blit(panel_surface, panel_rect)

    global play_button_rect, back_button_rect

    unscale_play = Globals.IMAGES['BUTTON']['START']
    play_button_img = p.transform.smoothscale(unscale_play, (
        int(unscale_play.get_width() * Globals.BUTTON_RATIO), int(unscale_play.get_height() * Globals.BUTTON_RATIO)))
    play_button_rect = play_button_img.get_rect(center=(342, 550))
    screen.blit(play_button_img, play_button_rect)

    unscala_back = Globals.IMAGES['BUTTON']['BACK']
    back_button_img = p.transform.smoothscale(unscala_back, (
        int(unscala_back.get_width() * Globals.BUTTON_RATIO), int(unscala_back.get_height() * Globals.BUTTON_RATIO)))
    back_button_rect = play_button_img.get_rect(center=(136, 550))
    screen.blit(back_button_img, back_button_rect)


def get_and_upload_hs(score):
    file_name = 'highscore.txt'
    result = 0
    if os.path.isfile(file_name):
        with open(file_name, 'r+') as f:
            file_hs = f.read()
            f.seek(0)
            max_hs = max(int(score), int(file_hs))
            result = max_hs
            f.write(str(max_hs))
            f.truncate()
    else:
        with open(file_name, "w") as f:
            f.write(str(score))
            result = score

    return result


def reset_setting():
    global is_ground_visible, game_Y, play_button_rect, back_button_rect
    Globals.GAME_SPEED = 2
    game_Y = 0
    is_ground_visible = True
    play_button_rect = None
    back_button_rect = None


def clostest_obstical(jojo, armatures, hammers, dir):
    min_y = 2 ** 32 - 1
    min_armature = armatures.sprites()[0]
    min_hammer = hammers.sprites()[0]
    for i, sprite in enumerate(armatures.sprites()):
        if sprite.rect.top < jojo.y and sprite.dir == dir:
            if min_y > jojo.y - sprite.rect.top:
                min_y = jojo.y - sprite.rect.top
                min_armature = sprite
                min_hammer = hammers.sprites()[i]
    return min_armature, min_hammer


def game_AI(genomes, config):
    global clock, game_Y
    ge = []
    nets = []
    jojo_group = p.sprite.Group()

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        jojo = Jojo()
        jojo.change_jojo_skin()
        p.sprite.Group.add(jojo_group, jojo)
        ge.append(genome)

    swing_iter = 0

    armatures_group = p.sprite.Group()
    hammers_group = p.sprite.Group()

    game_Y = 0
    score = 0

    while True:

        game_Y += Globals.GAME_SPEED
        swing_iter = (swing_iter + Globals.HAMMER_SPEED) % 60
        draw_background(screen, game_Y)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == BLINK_ANIMATION:
                for jojo in jojo_group.sprites():
                    jojo.blink_animation()

            if event.type == FAN_ANIMATION:
                for jojo in jojo_group.sprites():
                    jojo.fan_animation()

            if event.type == SPAWN_ARMATURE:
                armatures_list = armatures_group.sprites()
                hammers_list = hammers_group.sprites()

                for i in range(len(armatures_list)):
                    arm = armatures_list[i]
                    ham = hammers_list[i]
                    if arm.rect.top > Globals.HEIGHT:
                        armatures_group.remove(arm)
                        hammers_group.remove(ham)
                rand_x = random.randint(80, Globals.WIDTH - Globals.ARMATURE_SPACE - 80)
                p.sprite.Group.add(armatures_group, Armature(rand_x, -1))
                p.sprite.Group.add(armatures_group, Armature(rand_x, 1))
                p.sprite.Group.add(hammers_group, Hammer(rand_x, swing_iter, -1))
                p.sprite.Group.add(hammers_group, Hammer(rand_x, swing_iter, 1))

        index = len(jojo_group.sprites()) - 1
        for jojo in reversed(jojo_group.sprites()):
            if jojo.is_hit_wall() or jojo.is_hit_armature(armatures_group) or jojo.is_hit_hammer(hammers_group):
                ge[index].fitness -= 1
                jojo_group.remove(jojo)
                nets.pop(index)
                ge.pop(index)
            index -= 1

        if len(jojo_group) == 0:
            break
        else:
            pass
            # print(len(jojo_group))

        for i, jojo in enumerate(jojo_group.sprites()):
            ge[i].fitness += 0.1

            if len(armatures_group) > 0:
                left_armature, left_hammer = clostest_obstical(jojo, armatures_group, hammers_group, -1)
                right_armature, right_hammer = clostest_obstical(jojo, armatures_group, hammers_group, 1)

                if jojo.dir > 0:
                    output = nets[i].activate((
                        jojo.rect.topleft[0],
                        # right_armature.rect.topleft[0],
                        # right_hammer.rect.topleft[0]
                        # abs(jojo.rect.topleft[0] - right_armature.rect.topleft[0]),
                        # abs(jojo.rect.topleft[0] - right_hammer.rect.bottomleft[0])

                        abs(jojo.x - right_armature.rect.topleft[0]),
                        abs(jojo.x - right_hammer.rect.bottomleft[0])
                    ))

                else:
                    output = nets[i].activate((
                        jojo.rect.topright[0],
                        # left_armature.rect.topright[0],
                        # left_hammer.rect.topright[0]
                        # abs(jojo.rect.topright[0] - left_armature.rect.topright[0]),
                        # abs(jojo.rect.topright[0] - left_hammer.rect.bottomright[0])
                        abs(jojo.x - left_armature.rect.topright[0]),
                        abs(jojo.x - left_hammer.rect.bottomright[0])
                    ))

                p.draw.line(screen, (255, 0, 0), (jojo.x, jojo.y), left_armature.rect.midright, 2)
                p.draw.line(screen, (255, 0, 0), (jojo.x, jojo.y), right_armature.rect.midleft, 2)

                p.draw.line(screen, (255, 255, 0), (jojo.x, jojo.y), left_hammer.rect.bottomright, 2)
                p.draw.line(screen, (255, 255, 0), (jojo.x, jojo.y), right_hammer.rect.bottomleft, 2)
                # p.draw.rect(screen, (255, 255, 0), left_hammer.rect)
                # p.draw.rect(screen, (255, 255, 0), right_hammer.rect)

                if output[0] > 0.5:
                    jojo.changeDir()

            else:
                jojo.changeDir()

        score = check_score(score, jojo_group.sprites()[0], armatures_group)
        ds = int2image(score, 'U')
        screen.blit(ds, ds.get_rect(center=(Globals.WIDTH // 2, 50)))

        jojo_group.update()
        armatures_group.update()
        hammers_group.update()

        jojo_group.draw(screen)
        armatures_group.draw(screen)
        hammers_group.draw(screen)

        p.display.update()
        clock.tick(Globals.MAX_FPS)


def game_human(jojo_group=None, skin_index=-1):
    global clock, game_Y, play_button_rect, back_button_rect

    if jojo_group is None:
        jojo_group = p.sprite.GroupSingle(Jojo())
    jojo = jojo_group.sprites()[0]

    if skin_index != -1:
        jojo.change_jojo_skin(skin_index)
    armatures_group = p.sprite.Group()
    hammers_group = p.sprite.Group()

    swing_iter = 0
    score = 0
    alive = True
    high_score = 0
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = p.mouse.get_pos()

                if play_button_rect is not None and play_button_rect.collidepoint(mouse_pos):
                    reset_setting()
                    game_human(skin_index=jojo.jojo_skin)
                    break

                if back_button_rect is not None and back_button_rect.collidepoint(mouse_pos):
                    reset_setting()
                    main()
                    break

            if event.type == p.KEYDOWN:
                jojo.changeDir()

            if event.type == BLINK_ANIMATION:
                jojo.blink_animation()

            if event.type == FAN_ANIMATION:
                jojo.fan_animation()

            if event.type == SPAWN_ARMATURE:
                armatures_list = armatures_group.sprites()
                hammers_list = hammers_group.sprites()

                for i in range(len(armatures_list)):
                    arm = armatures_list[i]
                    ham = hammers_list[i]
                    if arm.rect.top > Globals.HEIGHT:
                        armatures_group.remove(arm)
                        hammers_group.remove(ham)

                rand_x = random.randint(80, 200)
                p.sprite.Group.add(armatures_group, Armature(rand_x, -1))
                p.sprite.Group.add(armatures_group, Armature(rand_x, 1))
                p.sprite.Group.add(hammers_group, Hammer(rand_x, swing_iter, -1))
                p.sprite.Group.add(hammers_group, Hammer(rand_x, swing_iter, 1))

        if (jojo.is_hit_wall() or jojo.is_hit_armature(armatures_group) or jojo.is_hit_hammer(hammers_group)) and alive:
            alive = False
            high_score = get_and_upload_hs(score)

        if alive:
            game_Y += Globals.GAME_SPEED
            draw_background(screen, game_Y)

        else:
            draw_background(screen, game_Y)
            Globals.GAME_SPEED = 0
            jojo_group.remove(jojo)

        score = check_score(score, jojo, armatures_group)
        ds = int2image(score, 'U')
        screen.blit(ds, ds.get_rect(center=(Globals.WIDTH // 2, 50)))

        swing_iter = (swing_iter + Globals.HAMMER_SPEED) % 60

        jojo_group.update()
        armatures_group.update()
        hammers_group.update()

        jojo_group.draw(screen)
        armatures_group.draw(screen)
        hammers_group.draw(screen)

        if not alive:
            draw_game_over(screen, score, int2image(score, 'L'), int2image(high_score, 'L'))
        p.display.update()
        clock.tick(Globals.MAX_FPS)


def main():
    global color

    jojo = Jojo()
    jojo_group = p.sprite.GroupSingle(jojo)

    color = random.randint(0, 2)
    title_index = 0

    unscale_jojo = Globals.IMAGES['BUTTON']['CHANGE']
    unscale_start = Globals.IMAGES['BUTTON']['START']
    unscale_ai_start = Globals.IMAGES['BUTTON']['AI_START']

    change_jojo = p.transform.smoothscale(unscale_jojo,
                                          (unscale_jojo.get_width() * Globals.BUTTON_RATIO,
                                           unscale_jojo.get_height() * Globals.BUTTON_RATIO))
    start_button = p.transform.smoothscale(unscale_start,
                                           (unscale_start.get_width() * Globals.BUTTON_RATIO,
                                            unscale_start.get_height() * Globals.BUTTON_RATIO))
    start_ai_button = p.transform.smoothscale(unscale_ai_start, (
        unscale_ai_start.get_width() * Globals.BUTTON_RATIO, unscale_ai_start.get_height() * Globals.BUTTON_RATIO))

    total_space_rect = change_jojo.get_width() + start_button.get_width() + start_ai_button.get_width()
    total_gap = Globals.WIDTH - total_space_rect
    single_gap = total_gap // (3 * 2)

    buttons_y = Globals.HEIGHT - Globals.IMAGES['GROUND'].get_height() // 2 - change_jojo.get_height() // 2 + Globals.HEIGHT * Globals.GRASS_RATIO

    rect_change_jojo = change_jojo.get_rect(topleft=(single_gap, buttons_y))
    rect_start_button = start_button.get_rect(topleft=(rect_change_jojo.right + single_gap * 2, buttons_y))
    rect_start_ai_button = start_ai_button.get_rect(topright=(Globals.WIDTH - single_gap, buttons_y))

    while True:
        draw_background(screen, 0)

        current_title = Globals.IMAGES['TITLE'][title_index]
        rect_title = current_title.get_rect(center=(Globals.WIDTH // 2, 150))
        screen.blit(current_title, rect_title)

        screen.blit(change_jojo, rect_change_jojo)
        screen.blit(start_button, rect_start_button)
        screen.blit(start_ai_button, rect_start_ai_button)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = p.mouse.get_pos()
                if rect_change_jojo.collidepoint(mouse_pos):
                    jojo.change_jojo_skin(-2)

                if rect_start_button.collidepoint(mouse_pos):
                    game_human(jojo_group=jojo_group)
                    jojo = Jojo()
                    jojo_group.add(jojo)

                if rect_start_ai_button.collidepoint(mouse_pos):
                    AI()
                    reset_setting()

        title_index += 1
        if title_index == 4:
            title_index = 0

        #jojo_group.update(False)
        jojo_group.draw(screen)
        p.display.update()
        clock.tick(len(Globals.IMAGES['TITLE']) * 3)


def AI():
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(False))

    # Run for up to 25 generations.
    population.run(game_AI, 25)


def sprit():
    while True:

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
        screen.fill((255,255,255))

        screen.blit(Globals.IMAGES['BUTTON']['CHANGE'], (10, 20))
        screen.blit(Globals.IMAGES['BUTTON']['START'], (170, 20))
        screen.blit(Globals.IMAGES['BUTTON']['AI_START'], (10, 110))
        screen.blit(Globals.IMAGES['BUTTON']['BACK'], (170, 110))



        p.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
    #sprit()
