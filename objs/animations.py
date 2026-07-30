import os
import pygame


class Animation:
    def __init__(self: "Animation", character: str, vel: float) -> None:
        self.sprite_list: list[str] = []
        folder: str = f"src/sprites/{character}/"
        for sprite in os.listdir(folder):
            full_path: str = os.path.join(folder, sprite)
            if os.path.isfile(full_path):
                self.sprite_list.append(f"{folder}{sprite}")
        self.sprite_list.sort()
        self.index: float = 0
        self.vel: float = vel
        self.size: tuple[int, int] = (pygame.image
                                      .load(self.sprite_list[0]).size)

    def get_next_frame_path(self: "Animation") -> str:
        ret: str = self.sprite_list[int(self.index)]
        self.__move_index()
        return (ret)

    def get_width(self: "Animation") -> int:
        return (self.size[0])

    def get_height(self: "Animation") -> int:
        return (self.size[1])

    def __move_index(self: "Animation") -> None:
        self.index += self.vel
        if (self.index > len(self.sprite_list) - 1):
            self.index = 0
