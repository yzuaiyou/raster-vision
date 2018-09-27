import random

import click
import numpy as np
import rasterio
from rasterio.transform import from_origin

from rastervision.core.box import Box
from rastervision.core.class_map import ClassItem, ClassMap
from rastervision.data.utils import color_to_triple


def make_image(extent, chip_size, class_map):
    windows = extent.get_windows(chip_size, chip_size)
    nb_channels = 3
    image = np.zeros((extent.get_height(), extent.get_width(), nb_channels))
    image = image.astype(np.uint8)

    for window in windows:
        class_item = random.choice(class_map.get_items())
        color = class_item.color

        image[window.ymin:window.ymax, window.xmin:window.xmax, :] = \
            np.array(color_to_triple(color))[np.newaxis, np.newaxis, :]

    return image


def save_image(image, image_path):
    # save image as geotiff centered in philly
    transform = from_origin(-75.163506, 39.952536, 0.000001, 0.000001)
    height, width, nb_channels = image.shape

    with rasterio.open(
            image_path,
            'w',
            driver='GTiff',
            height=height,
            transform=transform,
            crs='EPSG:4326',
            compression=rasterio.enums.Compression.none,
            width=width,
            count=nb_channels,
            dtype='uint8') as dst:
        for channel_ind in range(0, nb_channels):
            dst.write(image[:, :, channel_ind], channel_ind + 1)


@click.command()
@click.argument('image_path')
@click.argument('labels_path')
def generate_scene(image_path, labels_path):
    """Generate a synthetic semantic segmentation scene.

    This is useful for generating synthetic scenes for testing purposes.
    """
    class_map = ClassMap([
        ClassItem(1, name='red', color='red'),
        ClassItem(2, name='green', color='green')
    ])

    # make extent that's divisible by chip_size
    chip_size = 300
    y_len = 2
    x_len = 2
    ymax = y_len * chip_size
    xmax = x_len * chip_size
    extent = Box(0, 0, ymax, xmax)

    image = make_image(extent, chip_size, class_map)
    save_image(image, image_path)
    save_image(image, labels_path)


if __name__ == '__main__':
    generate_scene()
