class Calculator:
    @staticmethod
    def center(screen_size: tuple[int, int],
               img_size: tuple[int, int],
               x_modifier: int = 0,
               y_modifier: int = 0) -> tuple[int, int]:
        x: int = (int(screen_size[0] / 2)) - (int(img_size[0] / 2))
        y: int = (int(screen_size[1] / 2)) - (int(img_size[1] / 2))
        return ((x + x_modifier, y + y_modifier))
