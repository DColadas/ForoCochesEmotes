from PIL import Image
import glob
import os

# Routes
IMAGE_ROUTE = "emotes"
EXPORT_ROUTE = "saved"

# New image size parameters
FULL_SIZE = 512
MARGIN = 0
FINAL_SIZE = FULL_SIZE - MARGIN * 2

def getNewSize(oldSize, newHeight):
    """
    Returns a tuple with a size that keeps the old aspect ratio.
    """
    newWidth  = int(newHeight * oldSize[0] / oldSize[1])
    return (newWidth, newHeight)


if __name__ == "__main__":
    # Create output directory
    if not os.path.exists(EXPORT_ROUTE):
        os.makedirs(EXPORT_ROUTE)

    # Get every image,
    images = {}
    for filename in glob.glob(f"{IMAGE_ROUTE}/*.gif"):
        name = os.path.splitext(os.path.basename(filename))[0]
        images[name] = Image.open(filename)

    # resize it and export it to PNG
    for name, im in images.items():
        size = getNewSize(im.size, FINAL_SIZE)
        im = im.resize(size)
        im.save(f"{EXPORT_ROUTE}/{name}.png")
