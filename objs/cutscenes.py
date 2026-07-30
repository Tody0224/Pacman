import cv2
import numpy
import pygame
from pygame import Surface, surfarray, transform, display


class Cutscenes:
    @staticmethod
    def game_opening(screen: Surface,
                     virtual_screen: Surface,
                     original_screen_size: tuple[int, int],
                     is_fullscreen) -> bool:
        clock: pygame.time.Clock = pygame.time.Clock()
        opening: cv2.VideoCapture = cv2.VideoCapture("src/videos/opening.mp4")
        video_fps: float = opening.get(cv2.CAP_PROP_FPS)
        pygame.mixer.music.load("src/videos/opening.mp3")
        running: bool = True
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        while (running):
            time_ms: int = pygame.mixer.music.get_pos()
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
                        if (not is_fullscreen):
                            is_fullscreen = True
                            virtual_screen = transform.scale(virtual_screen,
                                                             (1920, 1080))
                            display.set_mode((1920,1080), pygame.FULLSCREEN)
                        else:
                            is_fullscreen = False
                            virtual_screen = transform.scale(virtual_screen,
                                                             original_screen_size)
                            display.set_mode(original_screen_size)
            frame_rgb: numpy.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rotated: numpy.ndarray = numpy.rot90(frame_rgb)
            frame_corrected: numpy.ndarray = cv2.flip(frame_rotated, 0)
            frame_surface: Surface = surfarray.make_surface(frame_corrected)
            virtual_screen.blit(frame_surface, (0, 70))
            screen.blit(virtual_screen)
            pygame.display.update()
            clock.tick(60)
        virtual_screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.mixer.music.stop()
        return (True)
