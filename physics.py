from objects import max_fuel, explosion_fig, height, player_y
import pygame
crash_sound = pygame.mixer.Sound("crash.wav")

def check_scenario_collision(p1, bg_margins):  # checks if player has collided with background elements
    player_mask = p1.get_mask()
    y_margin = []
    masks = []
    x_margin = []
    for list in bg_margins.get_mask():
        if list[0][1] >= player_y - height:
            for i in list:
                x_margin.append(i[0])
                y_margin.append(i[1])
                masks.append(i[2])
    distance = []
    for i in range(len(masks)):
        distance.append((int(x_margin[i] - p1.x_pos), int(y_margin[i] - p1.y_pos)))
    collision = []
    for i in range(len(masks)):
        collision.append(player_mask.overlap(masks[i], distance[i]))
        if (collision[i]):
            pygame.mixer.Sound.play(crash_sound)
            return True
    return False


def check_scenario_fuel_collision(bg_margins, fuel):  # checks if new fuel tank coincides with any background elements
    fuel_mask = fuel.get_mask()
    y_margin = []
    masks = []
    x_margin = []

    for list in bg_margins.get_mask():
        if list[0][1] <= fuel.y_pos:
            for i in list:
                x_margin.append(i[0])
                y_margin.append(i[1])
                masks.append(i[2])
    distance = []
    for i in range(len(masks)):
        distance.append((int(x_margin[i] - fuel.x_pos), int(y_margin[i] - fuel.y_pos)))
    collision = []
    for i in range(len(masks)):
        collision.append(fuel_mask.overlap(masks[i], distance[i]))
        if (collision[i]):
            return True
    return False


def check_enemy_collision(p1, enemy_list):  # checks if player has collides with an enemy
    player_mask = p1.get_mask()
    for enemy in enemy_list:
        enemy_mask = enemy.get_mask()
        distance = (int(enemy.x_pos - p1.x_pos), int(enemy.y_pos-p1.y_pos))
        collision = player_mask.overlap(enemy_mask, distance)
        if collision:
            pygame.mixer.Sound.play(crash_sound)
            return True
    return False


def check_bullet_kill(p1, enemy_list, screen):  # checks if any bullet has reached an enemy
    for enemy in enemy_list:
        for bullet in p1.bullet_list:
            if (bullet.y_pos - enemy.y_pos < enemy.height and enemy.y_pos - bullet.y_pos < bullet.height) and (bullet.x_pos - enemy.x_pos < enemy.width and enemy.x_pos - bullet.x_pos < bullet.width):
                screen.blit(explosion_fig, (enemy.x_pos, enemy.y_pos))
                pygame.display.flip()
                enemy_list.remove(enemy)
                p1.bullet_list.remove(bullet)
                pygame.mixer.Sound.play(crash_sound)
                p1.score += 100
                break


def check_fuel_collision(p1, fuel_list):
    player_mask = p1.get_mask()
    for fuel in fuel_list:
        fuel_mask = fuel.get_mask()
        distance = (int(fuel.x_pos - p1.x_pos), int(fuel.y_pos - p1.y_pos))
        collision = player_mask.overlap(fuel_mask, distance)
        if collision:
            p1.fuel = max_fuel
            fuel_list.remove(fuel)
            break


def check_bullet_fuel_collision(p1, fuel_list):  # checks if any bullet has reached an fuel
    for fuel in fuel_list:
        for bullet in p1.bullet_list:
            if (bullet.y_pos - fuel.y_pos < fuel.height and fuel.y_pos - bullet.y_pos < bullet.height) and (bullet.x_pos - fuel.x_pos < fuel.width and fuel.x_pos - bullet.x_pos < bullet.width):
                fuel_list.remove(fuel)
                pygame.mixer.Sound.play(crash_sound)
                p1.bullet_list.remove(bullet)
                p1.score += 100
                break