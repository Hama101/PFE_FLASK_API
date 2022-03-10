import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
import cv2
from skimage import io


def predict_image(image_path="ojja-shakshuka-2.jpg"):
    labelmap_url = "https://www.gstatic.com/aihub/tfhub/labelmaps/aiy_food_V1_labelmap.csv"
    input_shape = (224, 224)

    m = hub.KerasLayer(
        "https://tfhub.dev/google/aiy/vision/classifier/food_V1/1")

    image = np.asarray(io.imread(image_path), dtype="float")
    image = cv2.resize(image, dsize=input_shape, interpolation=cv2.INTER_CUBIC)
    # Scale values to [0, 1].
    image = image / image.max()
    # The model expects an input of (?, 224, 224, 3).
    images = np.expand_dims(image, 0)
    output = m(images)
    predicted_index = output.numpy().argmax()
    classes = list(pd.read_csv(labelmap_url)["name"])
    return classes[predicted_index]


if __name__ == "__main__":
    import time
    start_time = time.time()
    predict_image()
    print("--- %s seconds ---" % (time.time() - start_time))
