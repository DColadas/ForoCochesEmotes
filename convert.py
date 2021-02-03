import os
import shutil
import glob
from apng import APNG
from PIL import Image
from typing import List, Tuple, Optional

# Routes
IMAGE_ROUTE = "gifs"
EXPORT_ROUTE = "saved"
TEMP_ROUTE = "_temp_pngs"

# New image parameters
DEFAULT_FRAMERATE = 10   # 10 fps
FULL_SIZE = 512
MARGIN = 0
FINAL_SIZE = FULL_SIZE - MARGIN * 2


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


def decompose(image: Image, name: str, newSize: Optional[Tuple[int, int]] = None) -> List[str]:
    """
    Decomposes an image into its scaled PNG frames.
    If ${newSize} is None, no scaling is done
    Returns a list with the routes of the exported images.
    """
    nameList = []
    frame = 0
    initialFrame = image.tell()
    image.seek(0)
    while True:
        try:
            imageName = f"{TEMP_ROUTE}/{name}_{frame}.png"
            nameList.append(imageName)
            if size is not None:
                im = image.resize(newSize)
                im.save(imageName)
            else:
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
    duration = gif.info["duration"]
    return 1000 / (duration if duration else DEFAULT_FRAMERATE)


def getNewSize(oldSize: int, newHeight: int) -> Tuple[int, int]:
    """
    Returns a tuple with a size that keeps the old aspect ratio.
    """
    newWidth = int(newHeight * oldSize[0] / oldSize[1])
    return (newWidth, newHeight)


if __name__ == "__main__":
    # Create directories
    if not os.path.exists(EXPORT_ROUTE):
        os.makedirs(EXPORT_ROUTE)
    if not os.path.exists(TEMP_ROUTE):
        os.makedirs(TEMP_ROUTE)

    # Get every GIF (single- or multi-frame)
    images = {}
    for filename in glob.glob(f"{IMAGE_ROUTE}/*.gif"):
        name = os.path.splitext(os.path.basename(filename))[0]
        images[name] = Image.open(filename)

    # Resize every static image and export it to PNG
    for name, im in images.items():
        exportName = f"{EXPORT_ROUTE}/{name}.png"
        size = getNewSize(im.size, FINAL_SIZE)
        if isAnimated(im):
            # Animated GIF
            nameList = decompose(im, name, size)
            png = APNG.from_files(
                nameList, delay=int(getConstantFramerate(im)))
            png.save(exportName)
        else:
            # Single-frame GIF
            im = im.resize(size)
            im.save(exportName)

    # Delete the temporary directory
    shutil.rmtree(TEMP_ROUTE)
