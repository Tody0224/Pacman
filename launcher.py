import os
import threading
from typing import Optional
from objs import Pac_ser, App
from configparser import ConfigParser
from flask import Flask, request, send_from_directory, Response


app: Flask = Flask(__name__, static_folder="launcher", static_url_path="")


@app.route("/")
def home() -> Response:
    return (send_from_directory("launcher", "index.html"))


@app.route("/play", methods=["POST"])
def play() -> Response:
    resolution: Optional[str] = request.form.get("screen")
    fullscreen: Optional[str] = request.form.get("fullscreen")

    ini_maker: ConfigParser = ConfigParser()
    ini_maker["SETTINGS"] = {"resolution": resolution,
                             "fullscreen": str(bool(fullscreen))}

    with open("config.ini", "w") as f:
        ini_maker.write(f)
    return (Response("OK", status=200))


def run_server() -> None:
    app.run(host="localhost", port=5000)


def main() -> None:
    threading.Thread(target=run_server, daemon=True).start()
    os.system(
        "google-chrome "
        "--app=http://127.0.0.1:5000 "
        "--window-size=800,600 "
        "--disable-infobars "
        "--disable-session-crashed-bubble "
        "--disable-features=ChromeWhatsNewUI "
        "--no-first-run "
        "--no-default-browser-check "
        "--disable-notifications "
        "--disable-component-update "
        "--disable-background-networking"
    )
    return

if (__name__ == "__main__"):
    main()
