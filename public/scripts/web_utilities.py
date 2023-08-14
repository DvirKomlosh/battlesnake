"""Generic useful utilities for creating games with PyScript."""

import asyncio
from typing import Callable, Union

import pyscript
from js import Audio, Element, FontFace, Image, document, window


class Alignment:
    CENTER = 0
    TOP_LEFT = 1


def download_image(src: str) -> Image:
    result = asyncio.Future()
    image = Image.new()
    image.onload = lambda _: result.set_result(image)
    image.src = src
    return result


def download_images(sources: list[tuple[str, str]]) -> dict[str, Image]:
    remaining_images: list[str] = []
    result = asyncio.Future()

    images: dict[str, Image] = {}
    remaining = len(sources)

    def add_image(image):
        nonlocal remaining
        nonlocal remaining_images
        src = image.currentTarget.src
        to_remove = None
        for image in remaining_images:
            if image in src:
                to_remove = image
                break
        if to_remove:
            remaining_images.remove(to_remove)
        else:
            print(str(image) + " not in remaining")

        remaining -= 1
        print(remaining_images)
        if remaining == 0:
            result.set_result(images)

    for key, src in sources:
        image = Image.new()
        images[key] = image
        remaining_images.append(src)
        image.onload = lambda _: add_image(_)
        image.onerror = lambda _: print(f"Failed to fetch {src}")
        image.src = src

    return result


def get_element(id: str) -> Element:
    """Wrapper for JS getElementById."""
    return document.getElementById(id)


def get_breakpoint() -> int:
    value = document.getElementById("breakpoint").value
    if value == "":
        return -1
    return int(value)


def show_alert(
    title: str, alert: str, color: str, icon: str, limit_time: int = 5000, is_code=True
):
    if hasattr(window, "showAlert"):
        window.showAlert(title, alert, color, icon, limit_time, is_code)


def set_results(player_names: list[str], places: list[int], map: str):
    if hasattr(window, "setResults"):
        window.setResults(player_names, places, map)


def set_many_results(player_names: list[str], places: list[int], map: str, many: int):
    if hasattr(window, "setManyResults"):
        window.setManyResults(player_names, places, map, many)


def clear_many_results(player_names: list[str], map: str):
    if hasattr(window, "clearManyResults"):
        window.clearManyResults(player_names, map)


def should_play():
    return "Pause" in document.getElementById("playpause").textContent


def get_playback_speed():
    return 2 ** float(
        document.getElementById("timescale")
        .getElementsByClassName("mantine-Slider-thumb")
        .to_py()[0]
        .ariaValueNow
    )


SOUNDS: dict[str, Audio] = {}


def play_sound(sound: str):
    if sound not in SOUNDS:
        SOUNDS[sound] = Audio.new("/sounds/" + sound + ".mp3")

    SOUNDS[sound].cloneNode(True).play()


async def with_timeout(fn: Callable[[], None], timeout_seconds: float):
    async def f():
        fn()

    await asyncio.wait_for(f(), timeout_seconds)


class GameCanvas:
    """
    A nice wrapper around HTML Canvas for drawing map-based multiplayer games.
    """

    scale: float
    """The amount of real pixels in one map pixel"""

    def __init__(
        self,
        canvas: Element,
        map_image: Image,
        max_width: int,
        max_height: int,
        extra_height: int,
    ):
        self.canvas = canvas
        self.map_image = map_image
        self.extra_height = extra_height

        self.fit_into(max_width, max_height)

    def fit_into(self, max_width: int, max_height: int):
        while self.map_image.width == 0 or self.map_image.height == 0:
            raise Exception("Map image invalid!")
        aspect_ratio = self.map_image.width / (
            self.map_image.height + self.extra_height
        )
        width = min(max_width, max_height * aspect_ratio)
        height = width / aspect_ratio
        self.canvas.style.width = f"{width}px"
        self.canvas.style.height = f"{height}px"
        self.canvas.width = width * window.devicePixelRatio
        self.canvas.height = height * window.devicePixelRatio
        self.context = self.canvas.getContext("2d")
        self.context.textAlign = "center"
        self.context.textBaseline = "middle"
        self.scale = self.canvas.width / self.map_image.width

    def _translate_position(self, x: float, y: float):
        x *= self.scale
        y *= self.scale
        return x, y

    def _translate_width(self, width: float, aspect_ratio: float):
        """Aspect ratio: w/h"""
        width *= self.scale
        height = width / aspect_ratio
        return width, height

    def clear(self):
        """Clears the canvas and re-draws the players' maps"""
        self.context.clearRect(0, 0, self.canvas.width, self.canvas.height)
        self.context.fillStyle = "#fff"
        self.context.fillRect(0, 0, self.canvas.width, self.canvas.height)

        self.context.drawImage(
            self.map_image,
            0,
            0,
            self.map_image.width * self.scale,
            self.map_image.height * self.scale,
        )

    def draw_element(
        self,
        image: Image,
        x: int,
        y: int,
        width: int,
        direction: Union[float, None] = None,
        alignment=Alignment.CENTER,
    ):
        """
        Draws the given image on the specified player's board.
        Scaled to fit `width` in map pixels, be on position (`x`, `y`) in map pixels and face `direction`
        where 0 is no rotation and the direction is clockwise positive.
        """

        if direction is None:
            direction = 0

        x, y = self._translate_position(x, y)
        width, height = self._translate_width(width, image.width / image.height)

        if alignment == Alignment.TOP_LEFT:
            x += width / 2
            y += height / 2

        self.context.save()
        self.context.translate(x, y)
        self.context.rotate(direction)
        self.context.translate(-width / 2, -height / 2)
        self.context.drawImage(image, 0, 0, width, height)
        self.context.restore()

    def draw_text(
        self,
        text: str,
        color: str,
        x: int,
        y: int,
        text_size=15,
        font="",
    ):
        if font != "":
            font += ", "
        x, y = self._translate_position(x, y)

        self.context.font = f"{text_size * self.scale}pt {font}system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif, 'Noto Emoji'"
        self.context.fillStyle = color
        self.context.fillText(text, x, y)

    @property
    def total_width(self):
        return self.map_image.width


async def load_font(name: str, url: str):
    ff = FontFace.new(name, f"url({url})")
    print("Created", ff, name, url)
    await ff.load()
    print("Loaded", ff, name, url)
    document.fonts.add(ff)
    print("Added", ff, name, url)


class Stub:
    def __init__(self, other):
        for key in dir(other):
            if key.startswith("_"):
                continue
            setattr(
                self,
                key,
                lambda *args, ctt=getattr(other, key), **kwargs: ctt(*args, **kwargs),
            )
