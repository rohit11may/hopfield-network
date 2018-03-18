import random

import pickle
from mnist import MNIST

DATASET_LOC = '../dataset/compressed'
EMNIST = 'digits'


class BinaryImage:
    def __init__(self, img, width=28, threshold=200):
        converted_image = []
        current_row = []
        for i in range(len(img)):
            if i % width == 0:
                converted_image.append(current_row)
                current_row = []
            if img[i] > threshold:
                current_row.append(1)
            else:
                current_row.append(0)
        self.img = converted_image

    def __repr__(self):
        return "\n".join(["".join(str(pixel) for pixel in row) for row in self.img])


def loadImages(dataset_loc=DATASET_LOC, emnist=EMNIST):
    mnData = MNIST(dataset_loc)
    mnData.select_emnist(emnist)

    print("Unzipping and loading data set...")
    images, labels = mnData.load_training()
    print("Finished loading data set...")

    index = random.randrange(0, len(images))  # choose an index ;-)
    print("Displaying image...")
    print("Number of images: %s" % len(images))

    return images, labels


def load_binary_images(loc="../dataset/bin.dat"):
    print("Loading binary images...")
    try:
        with open(loc, "rb") as f:
            loaded_images = pickle.load(f)
    except Exception as e:
        print(str(e))
        loaded_images = []
    return loaded_images


def convert_to_binary_images(images):
    print("Converting images to binary...")
    return [BinaryImage(img) for img in images]


def save_images(images):
    print("Saving images to file...")
    with open("../dataset/bin.dat", "wb") as f:
        pickle.dump(images, f)
    print("Saved images.")


# Procedure to pre-process data set and convert to binary.
#
# images, labels = loadImages()
# binary_images = convert_to_binary_images(images)
# save_images(binary_images)

binary_images = load_binary_images()

