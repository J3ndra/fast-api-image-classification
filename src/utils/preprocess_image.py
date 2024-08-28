from PIL import Image
import numpy as np

def preprocess_image(image_path: str, target_size: tuple = (128, 128)):
    image = Image.open(image_path)
    image = image.resize(target_size)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image
