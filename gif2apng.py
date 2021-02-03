from apng import APNG
from PIL import Image
import os
from typing import List

TEMP_ROUTE = "_temp_pngs"
EXPORT_ROUTE = "saved"


def isAnimated(image: Image) -> bool:
    """ True if ${image} is animated (has more than 1 frame). """
    initialFrame = image.tell()
    animated = False
    try:
        image.seek(1)
        animated = True
    except EOFError:
        # Only has one frame: ignore
        pass
    image.seek(initialFrame)
    return animated


def decompose(image: Image, name: str) -> List[str]:
    """
    Decomposes an image into its scaled PNG frames.
    Returns a list with the routes of the exported images.
    {name}_{i}.png
    """
    nameList = []
    frame = 0
    initialFrame = image.tell()
    image.seek(0)
    while True:
        try:
            imageName = f"{TEMP_ROUTE}/{name}_{frame}.png"
            nameList.append(imageName)
            image.save(imageName)
            frame += 1
            image.seek(frame)
        except EOFError:
            # End gif
            break
    image.seek(initialFrame)
    return nameList


def getConstantFramerate(gif: Image) -> float:
    """ Returns the framerate of a PIL Image object with constant framerate """
    DEFAULT_FRAMERATE = 1000 / 10   # 10 fps
    duration = gif.info["duration"]
    return 1000 / duration if duration else DEFAULT_FRAMERATE


if __name__ == "__main__":
    # Create output directory
    if not os.path.exists(TEMP_ROUTE):
        os.makedirs(TEMP_ROUTE)

    # Open image
    name = "aaa"
    im = Image.open(f"{name}.gif")

    # Decompose
    nameList = decompose(im, name)

    APNG.from_files(nameList, delay=int(
        getConstantFramerate(im))).save(f"{name}.png")
