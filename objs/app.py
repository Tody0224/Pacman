import cv2
import numpy
import pygame
from pygame import (Surface, display, font,
                    image, transform, surfarray,
                    mixer as mix)
from .types import Coord
from .buttons import MenuSelect
from .animations import Animation
from .calculator import Calculator as Calc


class App:
    def __init__(self,
                 screen_size: tuple[int, int],
                 is_fullscreen: bool) -> None:
        pygame.init()
        display.set_caption("Pac-Man Collection")
        display.set_icon(image.load("src/icon.png"))
        self.is_fullscreen: bool = is_fullscreen
        if (self.is_fullscreen):
            self.screen: Surface = display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            self.screen = display.set_mode(screen_size)
        if ((self.is_fullscreen) and (screen_size == (1920, 1080))):
            self.original_screen_size: tuple[int, int] = (1920, 946)
        else:
            self.original_screen_size: tuple[int, int] = screen_size
        self.virtual_screen: Surface = Surface(screen_size)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.menu_bg_img: Surface = image.load("src/img/menu_bg.png")

    def set_fullscreen(self) -> None:
        if (not self.is_fullscreen):
            self.is_fullscreen = True
            self.virtual_screen = transform.scale(self.virtual_screen,
                                                  (1920, 1080))
            display.set_mode((1920, 1080), pygame.FULLSCREEN)
        else:
            self.is_fullscreen = False
            self.virtual_screen = transform.scale(self.virtual_screen,
                                                  self.original_screen_size)
            display.set_mode(self.original_screen_size)

    def game_opening(self) -> bool:
        clock: pygame.time.Clock = pygame.time.Clock()
        opening: cv2.VideoCapture = cv2.VideoCapture("src/videos/opening.mp4")
        video_fps: float = opening.get(cv2.CAP_PROP_FPS)
        mix.music.load("src/videos/opening.mp3")
        running: bool = True
        mix.music.set_volume(0.5)
        mix.music.play()
        while (running):
            time_ms: int = mix.music.get_pos()
            target_frame: int = int((time_ms / 1000.0) * video_fps)
            opening.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret: bool
            frame: numpy.ndarray
            ret, frame = opening.read()
            if (not (ret)):
                break
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return (False)
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE):
                        running = False
                    if (event.key == pygame.K_F11):
                        self.set_fullscreen()
            frame_rgb: numpy.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rotated: numpy.ndarray = numpy.rot90(frame_rgb)
            frame_corrected: numpy.ndarray = cv2.flip(frame_rotated, 0)
            frame_surface: Surface = surfarray.make_surface(frame_corrected)
            frame_coords: Coord = Calc.center(self.virtual_screen.size, frame_surface.size)
            self.virtual_screen.blit(frame_surface, frame_coords)
            self.screen.blit(self.virtual_screen, (0, 0))
            pygame.display.flip()
            self.virtual_screen.fill((0, 0, 0))
            clock.tick(60)
        self.virtual_screen.fill((0, 0, 0))
        pygame.display.flip()
        mix.music.stop()
        return (True)

    def __character_select(self) -> bool:
        running: bool = True
        text_font = font.Font("src/font/pixel.ttf", 50)
        text_font.set_bold(True)
        message: Surface = text_font.render("--- UNDER CONSTRUCTION ---",
                                            True, (250, 208, 57))
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    mix.music.stop()
                    running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_BACKSPACE):
                        return (False)
                    if (event.key == pygame.K_F11):
                        self.set_fullscreen()
            message_coords: Coord = Calc.center(self.virtual_screen.size,
                                                message.size)
            self.virtual_screen.blit(self.menu_bg_img, (0, 0))
            self.virtual_screen.blit(message, message_coords)
            self.screen.blit(self.virtual_screen, (0, 0))
            pygame.display.flip()
            self.virtual_screen.fill((0, 0, 0))
        return (True)

    def __settings(self) -> bool:
        running: bool = True
        text_font = font.Font("src/font/pixel.ttf", 50)
        text_font.set_bold(True)
        message: Surface = text_font.render("--- UNDER CONSTRUCTION ---",
                                            True, (250, 208, 57))
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    mix.music.stop()
                    running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_BACKSPACE):
                        return (False)
                    if (event.key == pygame.K_F11):
                        self.set_fullscreen()
            message_coords: Coord = Calc.center(self.virtual_screen.size,
                                                message.size)
            self.virtual_screen.blit(self.menu_bg_img, (0, 0))
            self.virtual_screen.blit(message, message_coords)
            self.screen.blit(self.virtual_screen, (0, 0))
            pygame.display.flip()
            self.virtual_screen.fill((0, 0, 0))
        return (True)

    def __readme(self) -> bool:
        running: bool = True
        text_font = font.Font("src/font/pixel.ttf", 50)
        text_font.set_bold(True)
        message: Surface = text_font.render("--- UNDER CONSTRUCTION ---",
                                            True, (250, 208, 57))
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    mix.music.stop()
                    running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_BACKSPACE):
                        return (False)
                    if (event.key == pygame.K_F11):
                        self.set_fullscreen()
            message_coords: Coord = Calc.center(self.virtual_screen.size,
                                                message.size)
            self.virtual_screen.blit(self.menu_bg_img, (0, 0))
            self.virtual_screen.blit(message, message_coords)
            self.screen.blit(self.virtual_screen, (0, 0))
            pygame.display.flip()
            self.virtual_screen.fill((0, 0, 0))
        return (True)

    def __leaderboards(self) -> None:
        running: bool = True
        text_font = font.Font("src/font/pixel.ttf", 50)
        text_font.set_bold(True)
        message: Surface = text_font.render("--- UNDER CONSTRUCTION ---",
                                            True, (250, 208, 57))
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    mix.music.stop()
                    running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_BACKSPACE):
                        return (False)
                    if (event.key == pygame.K_F11):
                        self.set_fullscreen()
            message_coords: Coord = Calc.center(self.virtual_screen.size,
                                                message.size)
            self.virtual_screen.blit(self.menu_bg_img, (0, 0))
            self.virtual_screen.blit(message, message_coords)
            self.screen.blit(self.virtual_screen, (0, 0))
            pygame.display.flip()
            self.virtual_screen.fill((0, 0, 0))
        return (True)

    def menu(self) -> None:
        logo: Surface = image.load("src/pac_man_logo.png")
        selections: list[MenuSelect] = [MenuSelect("Start",
                                                   self.__character_select,
                                                   True),
                                        MenuSelect("Settings",
                                                   self.__settings),
                                        MenuSelect("README",
                                                   self.__readme),
                                        MenuSelect("Leaderboard",
                                                   self.__leaderboards)]
        selec_index: int = 0
        selected: MenuSelect = selections[0]

        mix.music.load("src/music/menu.mp3")
        mix.music.set_volume(0.5)
        mix.music.play(-1)

        text_font: font.Font = font.Font("src/font/pixel.ttf", 20)
        font_chosen: font.Font = font.Font("src/font/pixel.ttf", 40)
        text_font.set_bold(True)
        font_chosen.set_bold(True)

        menu_sound_one: mix.Sound = mix.Sound("src/sfx/pacman/eat_dot_0.wav")
        menu_sound_two: mix.Sound = mix.Sound("src/sfx/pacman/eat_dot_1.wav")
        channel: mix.Channel = mix.Channel(0)

        pac_man: Animation = Animation("pacman", 0.3)
        power_pellet: Surface = image.load("src/sprites/common/"
                                           "power_pellet.png")
        power_pellet_index: int = 0

        running: bool = True
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    mix.music.stop()
                    running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key in [pygame.K_DOWN, pygame.K_RIGHT]):
                        selected.unselect()
                        selec_index += 1
                        if (selec_index > len(selections) - 1):
                            selec_index = 0
                        selected = selections[selec_index]
                        selected.select()
                        channel.play(menu_sound_one)
                        if (not (channel.get_busy())):
                            channel.play(menu_sound_two)
                    if (event.key in [pygame.K_UP, pygame.K_LEFT]):
                        selected.unselect()
                        selec_index -= 1
                        if (selec_index < 0):
                            selec_index = len(selections) - 1
                        selected = selections[selec_index]
                        selected.select()
                        channel.play(menu_sound_two)
                        if (not (channel.get_busy())):
                            channel.play(menu_sound_one)
                    if (event.key in [pygame.K_KP_ENTER, pygame.K_SPACE]):
                        if (selected.press()):
                            return
                    if (event.key == pygame.K_F11):
                        self.set_fullscreen()
            self.virtual_screen.blit(self.menu_bg_img, (0, 0))
            screen_size: tuple[int, int] = (self.virtual_screen.get_width(),
                                            self.virtual_screen.get_height())
            img_size: tuple[int, int] = logo.size
            logo_coords: Coord = Calc.center(screen_size,
                                             img_size,
                                             y_modifier=-(int(img_size[1]
                                                              / 5)))
            self.virtual_screen.blit(logo, logo_coords)
            y_modifier: int = logo_coords[1] + 100
            for button in selections:
                if (button.is_selected()):
                    color: tuple[int, int, int] = (250, 208, 57)
                    text: Surface = font_chosen.render(button.get_message(),
                                                       True, color)
                else:
                    color = (10, 25, 36)
                    text = text_font.render(button.get_message(),
                                            True, color)
                y_modifier += 60
                text_size: tuple[int, int] = text.size
                text_coords: Coord = Calc.center(screen_size,
                                                 text_size,
                                                 y_modifier=y_modifier)
                self.virtual_screen.blit(text, text_coords)
                if (button.is_selected()):
                    frame: Surface = image.load(pac_man.get_next_frame_path())
                    resized: Surface = transform.scale(frame,
                                                       (text.get_height(),
                                                        text.get_height()))
                    pac_coords: Coord = ((text_coords[0]
                                          - resized.size[0]),
                                         text_coords[1])
                    if (power_pellet_index % 50 in range(25)):
                        pellet_coords: Coord = (text_coords[0]
                                                + text.get_width(),
                                                text_coords[1])
                        resized_p: Surface = transform.scale(power_pellet,
                                                             (text.get_height(),
                                                              text.get_height()))
                        self.virtual_screen.blit(resized_p, pellet_coords)
                    self.virtual_screen.blit(resized, pac_coords)
            self.screen.blit(self.virtual_screen, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
            power_pellet_index += 1

    def run(self) -> None:
        if (not (self.game_opening())):
            return
        self.menu()
