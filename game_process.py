import pygame
import random
from death_screen import *
from parameters import *


def print_text(surface, text, x, y, font_size=24):
    font1 = pygame.font.SysFont('serif', font_size)
    to_print = font1.render(text, True, white)
    surface.blit(to_print, (x, y))


def game_process(surface, game_zone_w, screen_height, fps, clock):
    global point

    head_position = (int(game_zone_w/2), int(screen_height/2))
    body = list()
    body.append(head_position)
    snake_speed_x, snake_speed_y = 0, 0

    food_position = (random.choice(range(0, game_zone_w, 20)), random.choice(range(0, screen_height, 20)))
    point = 0
    counter = 0
    done = False

    while not done:
        clock.tick(fps)
        stop = set()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_w] or keystate[pygame.K_UP]:
                    snake_speed_x, snake_speed_y = 0, -20
                if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
                    snake_speed_x, snake_speed_y = 0, 20
                if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
                    snake_speed_x, snake_speed_y = -20, 0
                if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
                    snake_speed_x, snake_speed_y = 20, 0
                if keystate[pygame.K_SPACE]:
                    snake_speed_x, snake_speed_y = 0, 0
        counter += 1
        counter %= fps // 10
        if not counter:
            for i in range(len(body)-1, 0, -1):
                stuff_x, stuff_y = body[i-1]
                body[i] = (stuff_x % game_zone_w, stuff_y % screen_height)
                stop.add(body[i])

            stuff_x = head_position[0] + snake_speed_x
            stuff_y = head_position[1] + snake_speed_y
            head_position = (stuff_x, stuff_y)
            body[0] = (stuff_x % game_zone_w, stuff_y % screen_height)
            stop.add(body[0])

            if len(stop) < len(body):
                death_screen(surface, game_zone_w, fps, clock, point)

            if food_position == body[0]:
                point += 1

                # user_points = font1.render("Счет уже " + str(point), True, (255, 255, 255))
                if point == 1:
                    new_part_pos = (head_position[0]+snake_speed_x, head_position[1]+snake_speed_y)
                else:
                    new_part_pos = (2*body[-1][0]-body[-2][0], 2*body[-1][1]-body[-2][1])
                body.append(new_part_pos)

                stuff = False
                while not stuff:
                    food_position = (random.choice(range(0, game_zone_w, 20)), random.choice(range(0, screen_height, 20)))
                    if food_position not in body:
                        stuff = True

            surface.fill((0, 0, 0))
            for part in body:
                pygame.draw.rect(surface, (255, 0, 0), [part[0], part[1], 20, 20])
            pygame.draw.rect(surface, (255, 255, 255), [food_position[0], food_position[1], 20, 20])
            print_text(surface, 'Your score: ' + str(point), 520, 20, 24)

            pygame.draw.rect(surface, (255, 255, 255), [0, 0, game_zone_w, screen_height], width=1)
            pygame.draw.rect(surface, (255, 255, 255), [500, 0, 230, screen_height], width=1)
            pygame.display.flip()
