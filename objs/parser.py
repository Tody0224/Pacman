from .app import App
from configparser import ConfigParser


class Pac_ser:
    @staticmethod
    def app_init(config_path: str = "config.ini") -> App:
        config: ConfigParser = ConfigParser()
        config.read(config_path)

        config_res: str = config["SETTINGS"]["resolution"]
        width: int = int(config_res.split("x")[0])
        height: int = int(config_res.split("x")[1])
        is_fullscreen: bool = (config["SETTINGS"]["fullscreen"] == "True")
        if ((not (is_fullscreen)) and (height == 1080)):
            height = 946

        return (App((width, height), is_fullscreen))
