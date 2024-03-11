from typing import Union
import cv2
import numpy as np


def preprocess_image(
    source: Union[np.ndarray, str], image_size: int = 224
) -> np.ndarray:
    image: np.ndarray
    if isinstance(source, str):
        image = cv2.imread(source)
    else:
        image = source
    resized_img = cv2.resize(image, (image_size, image_size))
    img_gray_scale = np.expand_dims(
        cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), axis=-1
    )
    return img_gray_scale
