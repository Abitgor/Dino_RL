import pygame as pg
from Hero import Human,Hero
from Env import Environment
from config import *
from Graphics import Graphics
from image import Image
from CollisionLogic import CollisionLogic
from prop import Cactus,Bird

class GameEngine:
    def __init__(self):
        self.is_running = False
        self.human_player = True

        self.counter = 0

        self.human = None
        self.agent = None
        self.clock = None
        self.width = WIDTH
        self.height = HEIGHT

        if self.human_player:
            self.hero = Human()  # TODO replace Hero to Human
        else:
            self.hero = None  # TODO replace Hero to Agent

        self.environment = Environment()
        self.visible_obj = []
        self.screen = pg.display.set_mode((self.width, self.height))
        self.graphics = Graphics(self.screen)
        self.bg_image = []
        for image in BACKGROUND_IMAGE:
            self.bg_image.append(Image(image, [0, 0]))
        pg.init()

    def create_level(self):
        self.environment.spawn_prop(FIRST_SPAWN_DISTANCE)
        for props in range(0, NUMBER_OF_EXISTING_PROP):
            self.environment.spawn_prop()

    def draw_visible_obj(self):
        self.visible_obj = []
        self.visible_obj.append(self.hero)

        for prop in self.environment.prop_list:
            if prop.coord[0] < self.width - prop.size[0]:
                self.visible_obj.append(prop)

        for obj in self.visible_obj:
            if isinstance(obj, Hero):
                self.graphics.draw_obj(obj, (self.counter//5) % 6)
            elif isinstance(obj, Cactus):
                self.graphics.draw_obj(obj, 0)
            elif isinstance(obj, Bird):
                self.graphics.draw_obj(obj,(self.counter//12) % 2)

    def setup(self):
        self.create_level()
        self.clock = pg.time.Clock()

        self.is_running = True
        self.update()

    def key_checker(self):
        pressed = pg.key.get_pressed()
        key_arr = [pg.K_UP, pg.K_SPACE, pg.K_DOWN, pg.K_LCTRL]
        self.hero.change_state(pressed, key_arr)

    def collision_stuff(self):
        col_log = CollisionLogic

        cur_prop = self.environment.prop_list[0]

        return col_log.check_collision(self.hero, cur_prop)

    def update(self):
        while self.is_running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.bg_image[(self.counter//5) % 12].image, self.bg_image[(self.counter//5) % 12].rect)
            if self.collision_stuff():
                self.is_running = False

            self.key_checker()
            self.hero.update()

            self.environment.update()

            self.draw_visible_obj()
            self.counter += 1
            if self.counter == 60:
                self.counter = 0
            pg.display.flip()

            self.clock.tick(FPS)
