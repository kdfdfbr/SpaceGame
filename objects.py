import pygame
import random
import time

width = 750
height = 750
player_y = 650
max_fuel = 1000
resistance_to_sensibility = 15

initial_speed = 3
speed = initial_speed

bullet_fig = pygame.image.load("Images/bullet.png")
bullet_fig.convert()
background_fig = pygame.image.load("Images/background.png")
background_fig.convert()
player_fig = pygame.image.load("Images/player.png")
player_fig.convert()
player_fig= pygame.transform.scale(player_fig, (70, 70))
explosion_fig = pygame.image.load("Images/explosion.png")
explosion_fig.convert()
explosion_fig = pygame.transform.scale(explosion_fig, (65, 65))
fuel_fig = pygame.image.load("Images/fuel.png")
fuel_fig.convert()
fuel_fig = pygame.transform.scale(fuel_fig,(50,50))
img_helicopter = pygame.image.load("Images/helicopter_enemy.png")
img_helicopter.convert()
img_zeppelin = pygame.image.load("Images/zeppelin_enemy.png")
img_zeppelin.convert()
img_type1 = pygame.image.load("Images/margin_1_.png")
img_type1.convert()
img_type1 = pygame.transform.scale(img_type1, (60, 750))
img_type2l = pygame.image.load("Images/margin_2l.png")
img_type2l.convert()
img_type2l = pygame.transform.scale(img_type2l, (250, 750))
img_type2r = pygame.image.load("Images/margin_2r.png")
img_type2r = pygame.transform.scale(img_type2r, (250, 750))
img_type2r.convert()
img_type3 = pygame.image.load("Images/margin_3_central.png")
img_type3 = pygame.transform.scale(img_type3, (200, 300))
img_type3.convert()
img_type4 = pygame.image.load("Images/margin_4_central.png")
img_type4 = pygame.transform.scale(img_type4, (450, 500))
img_type4.convert()
fig_game_over = pygame.image.load("Images/Game_Over.png")
fig_game_over.convert()
fig_river_raid = pygame.image.load("Images/River_Raid.png")
fig_river_raid.convert()
fig_river_raid = pygame.transform.scale(fig_river_raid, (200, 200))
margin_left = [(0,img_type1), (0,img_type2l), (0,img_type1), (0,img_type1)]
margin_right = [(width - img_type1.get_width(),img_type1), (width-img_type2r.get_width(),img_type2r), (width - img_type1.get_width(),img_type1), (width - img_type1.get_width(),img_type1)]
margin_central = [0, 0, (width/2 - img_type3.get_width()/2,img_type3), (width/2 - img_type4.get_width()/2,img_type4)]
shoot_sound = pygame.mixer.Sound("gun_shoot.wav")


def draw_objects(screen, p1, bg_margins, enemy_list, fuel_list): # displays all the objects in the screen
    screen.blit(background_fig, (0, 0))
    bg_margins.draw(screen)
    p1.draw_score(screen)
    p1.draw_fuel(screen)
    p1.draw(screen)
    draw_enemies(enemy_list, screen)
    draw_fuel(fuel_list, screen)
    p1.draw_fps(screen)

def menu(p1, bg_margins, screen): # draws and control menu that is displayed in the beginning and after a game over
    # white color
    white_color = (255, 255, 255)

    # light shade of the button
    color_light = (170, 170, 170)

    # dark shade of the button
    color_dark = (100, 100, 100)

    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)

    # rendering a text written in
    # this font
    quit_text = smallfont.render('Quit', True, white_color)
    start_text = smallfont.render('Start', True, white_color)
    while (1):
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

                # checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height / 2 <= mouse[1] <= height / 2 + 40:
                    pygame.quit()
                if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                    break

        # fills the screen with the game background
        else:
            screen.blit(background_fig, (0, 0))
            bg_margins.draw(screen)
            p1.draw_score(screen)
            p1.draw_fuel(screen)
            screen.blit(fig_river_raid, (width / 2 - fig_river_raid.get_width() / 2, 50))
            p1.draw(screen)

            # if mouse is hovered on a button it changes to lighter shade
            if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(screen, color_light, [width / 2 - 70, height / 2, 140, 40])

            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 70, height / 2, 140, 40])

            if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height / 2 - 50 <= mouse[1] <= height / 2 + - 10:
                pygame.draw.rect(screen, color_light, [width / 2 - 70, height / 2 - 50, 140, 40])

            else:
                pygame.draw.rect(screen, color_dark, [width / 2 - 70, height / 2 - 50, 140, 40])

            # draw button text
            screen.blit(quit_text, (width / 2 - 30, height / 2))
            screen.blit(start_text, (width / 2 - 30, height / 2 - 50))

            # updates the frames of the game
            pygame.display.update()
            continue

        break


def game_over(p1,screen, bg_margins):
    screen.blit(fig_game_over, (0, 0))
    pygame.display.flip()
    p1.draw_score(screen)
    time.sleep(3)
    global speed
    speed = initial_speed
    menu(p1, bg_margins, screen)


def update_global_speed():
    global speed
    speed = speed + 0.0005


class Player:

    def __init__(self, x_pos, fuel, score):
        self.x_pos = x_pos
        self.y_pos = player_y
        self.fuel = fuel
        self.score = score
        self.bullet_list = []
        self.img = player_fig
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.font = pygame.font.SysFont("Arial", 18)
        self.clock = pygame.time.Clock()
        self.dt = 0 # used to stabilize fps

    def shoot(self):
        new_bullet = Bullet(self.x_pos + 30, self.y_pos)
        self.bullet_list.append(new_bullet)
        self.fuel -= 20
        pygame.mixer.Sound.play(shoot_sound)

    def move_right(self):
        self.x_pos += 5*self.dt/resistance_to_sensibility

    def move_left(self):
        self.x_pos -= 5*self.dt/resistance_to_sensibility

    def draw(self, screen):
        screen.blit(self.img,(self.x_pos, self.y_pos))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', 1, (0, 0, 0))
        textpos = text.get_rect(centerx = width / 2 - 100)
        screen.blit(text, textpos)

    def draw_fuel(self, screen): # displays the remaining fuel percentage
        font = pygame.font.Font(None, 36)
        text = font.render(f'Fuel: {self.fuel}', 1, (0, 0, 0))
        textpos = text.get_rect(centerx = width / 2 + 100)
        screen.blit(text, textpos)

    def draw_fps(self, screen):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        screen.blit(fps_text, (10, 0))

    def update_score(self): # displays the player score
        self.score += 1
        self.dt = self.clock.tick(60)


class Bullet:

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = bullet_fig.get_width()
        self.height = bullet_fig.get_height()
        self.img = bullet_fig

    def update(self, p1):
        self.y_pos -= 5*p1.dt/resistance_to_sensibility

    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))


class Enemy: # Father Class
    def __init__(self, x_pos, y_pos, dir, x_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.dir = dir
        self.x_speed = x_speed
        self.y0_mov = random.randrange(0, int(height/2))

    def flip(self):
        if self.dir == 'right':
            self.dir = 'left'
        elif self.dir == 'left':
            self.dir = 'right'


class Helicopter(Enemy):
    global speed

    def __init__(self, x_pos, y_pos, dir, x_speed = random.randrange(375, 425)/100):
        super().__init__(x_pos, y_pos, dir, x_speed)
        self.width = img_helicopter.get_width()
        self.height = img_helicopter.get_height()
        self.img = img_helicopter

    def update(self, p1):
        if self.dir == 'right' and self.y_pos > self.y0_mov:
            self.x_pos += self.x_speed*p1.dt/resistance_to_sensibility
        elif self.dir == 'left' and self.y_pos > self.y0_mov:
            self.x_pos -= self.x_speed*p1.dt/resistance_to_sensibility
        self.y_pos += speed*p1.dt/resistance_to_sensibility

    def draw(self,screen):
        if self.dir == 'left':
            flipped_img = pygame.transform.flip(self.img, True, False)
            screen.blit(flipped_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(self.img, (self.x_pos, self.y_pos))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Zeppelin(Enemy):
    global speed

    def __init__(self, x_pos, y_pos, dir, x_speed = random.randrange(275, 325)/100):
        super().__init__(x_pos, y_pos, dir, x_speed)
        self.width = img_zeppelin.get_width()
        self.height = img_zeppelin.get_height()
        self.img = img_zeppelin

    def update(self, p1):
        if self.dir == 'right' and self.y_pos > self.y0_mov:
            self.x_pos += self.x_speed*p1.dt/resistance_to_sensibility
        elif self.dir == 'left' and self.y_pos > self.y0_mov:
            self.x_pos -= self.x_speed*p1.dt/resistance_to_sensibility
        self.y_pos += speed*p1.dt/resistance_to_sensibility

    def draw(self, screen):
        if self.dir == 'left':
            screen.blit(self.img, (self.x_pos, self.y_pos))
        else:
            flipped_img = pygame.transform.flip(self.img, True, False)
            screen.blit(flipped_img, (self.x_pos, self.y_pos))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def update_enemies(enemy_list, p1): # updates the position from all the enemies in enemy_list and creates new enemies, if necessary
    if enemy_list == []:
        new_enemy = True
    else:
        new_enemy = (random.random() < 0.01/(len(enemy_list))**2.3) and enemy_list[-1].y_pos > 0
    if new_enemy:
        temp1 = random.choice([1, 2])
        temp2 = random.choice([1, 2])
        x0 = random.randrange(-max(img_zeppelin.get_width(), img_helicopter.get_width()), width)
        if temp1 == 1:
            if temp2 == 1:
                enemy = Helicopter(x0, -img_helicopter.get_height(), 'right')
            else:
                enemy = Helicopter(x0, -img_helicopter.get_height(), 'left')
        elif temp2 == 1:
            enemy = Zeppelin(x0, -img_zeppelin.get_height(), 'right')
        else:
            enemy = Zeppelin(x0, -img_zeppelin.get_height(), 'left')
        enemy_list.append(enemy)
    for enemy in enemy_list:
        enemy.update(p1)
        if enemy.y_pos > height:
            enemy_list.remove(enemy)
        elif (enemy.x_pos > width and enemy.dir == 'right') or (enemy.x_pos < -max(img_zeppelin.get_width(), img_helicopter.get_width()) and enemy.dir == 'left'):
            enemy.flip()


def draw_enemies(enemy_list, screen):
    for enemy in enemy_list:
        enemy.draw(screen)


class Fuel:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.img = fuel_fig
        self.height = fuel_fig.get_height()
        self.width = fuel_fig.get_width()

    def update(self, p1):
        self.y_pos += speed*p1.dt/resistance_to_sensibility

    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


from physics import check_scenario_fuel_collision


def update_fuel(fuel_list, p1, bg_margins, screen): # updates the position from all the enemies in enemy_list and creates new enemies, if necessary
    p1.fuel -= 1
    if fuel_list == [] and (random.random() < 0.0015 or p1.fuel< 250):
        while(1):
            x0 = random.randrange(img_type1.get_width(), width - fuel_fig.get_width()- img_type1.get_width())
            new_fuel = Fuel(x0, -fuel_fig.get_height())
            new_fuel.draw((screen))

            if(not check_scenario_fuel_collision(bg_margins,new_fuel)):
                fuel_list.append(new_fuel)
                break
    for fuel in fuel_list:
        fuel.update(p1)
        if fuel.y_pos > height:
            fuel_list.remove(fuel)


def draw_fuel(fuel_list, screen):
    for fuel in fuel_list:
        fuel.draw(screen)


class Margin:
    global speed
    num_of_blocks = 1

    def __init__(self):
        self.left_margin = [margin_left[0],margin_left[0], margin_left[1]] #list with 3*num_of_blocks objects
        self.right_margin = [margin_right[0],margin_right[0], margin_right[1]]
        self.central_margin = [margin_central[0],margin_central[0] , margin_central[1]]
        self.y = 0
        self.y_plot = [0,0,0]#list with 3*num_of_blocks elements that stores the y of plot of each one of the blockes

    def move(self, p1):
        self.y += speed*p1.dt/resistance_to_sensibility # updates reference position
        for i in range(3*self.num_of_blocks):
            self.y_plot[i] = (self.y + height * (self.num_of_blocks - 1 - i) / self.num_of_blocks) % (3 * height) - height / self.num_of_blocks
        if (self.y%(3*height) - 2*height < speed*p1.dt/resistance_to_sensibility and self.y%(3*height) - 2*height >= 0): # updates first set of blocks when it is not visible

            for j in range(self.num_of_blocks):
                temp = random.choice(range(len(margin_right)))
                self.left_margin[j] = margin_left[temp]
                self.right_margin[j] = margin_right[temp]
                self.central_margin[j] = margin_central[temp]
        elif (self.y%(3*height) < speed*p1.dt/resistance_to_sensibility): # updates second set of blocks when it is not visible
            for j in range(self.num_of_blocks, 2 * self.num_of_blocks):
                temp = random.choice(range(len(margin_right)))
                self.left_margin[j] = margin_left[temp]
                self.right_margin[j] = margin_right[temp]
                self.central_margin[j] = margin_central[temp]
        elif (self.y%(3*height) - height < speed*p1.dt/resistance_to_sensibility and self.y%(3*height) - height >= 0): # updates third set of blocks when it is not visible
            for j in range(2*self.num_of_blocks, 3 * self.num_of_blocks):
                temp = random.choice(range(len(margin_right)))
                self.left_margin[j] = margin_left[temp]
                self.right_margin[j] = margin_right[temp]
                self.central_margin[j] = margin_central[temp]

    def draw(self, screen):
        for i in range(3*self.num_of_blocks):
            screen.blit(self.left_margin[i][1], (self.left_margin[i][0], self.y_plot[i]))
            screen.blit(self.right_margin[i][1], (self.right_margin[i][0], self.y_plot[i]))
            if(self.central_margin[i] != 0):
                screen.blit(self.central_margin[i][1], (self.central_margin[i][0], self.y_plot[i]))

    def get_mask(self):
        list = []
        for i in range(len(self.y_plot)):
            if self.y_plot[i] >= - height and self.y_plot[i] <= player_y:
                if(self.central_margin[i] != 0):
                    list.append([(self.left_margin[i][0], self.y_plot[i], pygame.mask.from_surface(self.left_margin[i][1])), (self.central_margin[i][0], self.y_plot[i], pygame.mask.from_surface(self.central_margin[i][1])),
                            (self.right_margin[i][0], self.y_plot[i], pygame.mask.from_surface(self.right_margin[i][1]))])
                else:
                    list.append([(self.left_margin[i][0], self.y_plot[i], pygame.mask.from_surface(self.left_margin[i][1])),
                        (self.right_margin[i][0], self.y_plot[i], pygame.mask.from_surface(self.right_margin[i][1]))])
        return list

