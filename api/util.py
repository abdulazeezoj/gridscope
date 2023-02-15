# Define imports
import argparse
import base64
import os
from io import BytesIO
from typing import Any, List, Tuple

import cv2
import numpy as np
from PIL import Image

# Configs
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.txt")
LABELS = open(LABELS_PATH).read().strip().split("\n")

SCORE_THRESH: float = 0.5
NMS_THRESH: float = 0.45

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Font
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1


# Encode pillow image to base64 string
def encode_image(image):
    """
    Convert image to base64 string
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    image_enc = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return image_enc


def decode_image(image_enc):
    """
    Convert base64 string to PIL image
    """
    image_dec = base64.b64decode(image_enc)
    image = Image.open(BytesIO(image_dec))
    image = image.convert("RGB")

    return image


def render(image, *detection):
    """Draw text onto image at location."""

    # Convert image to numpy array.
    image = np.array(image)

    bboxes, confs, labels = detection
    for bbox, conf, label in zip(bboxes, confs, labels):
        left = bbox[0]
        top = bbox[1]
        width = bbox[2]
        height = bbox[3]
        text = f"{label} {conf:.2%}"

        cv2.rectangle(image, (left, top), (left + width, top + height), BLUE, 3 * THICKNESS)

        # Get text size.
        dim, baseline = cv2.getTextSize(text, FONT_FACE, FONT_SCALE, THICKNESS)
        # Use text size to create a BLACK rectangle.
        cv2.rectangle(
            image, (left, top), (left + dim[0], top - dim[1] - baseline), BLACK, cv2.FILLED
        )
        # Display text inside the rectangle.
        cv2.putText(
            image, text, (left, top - 5), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA
        )

    # Convert numpy array to pillow image.
    image = Image.fromarray(image)

    return image


def print_detection(bboxes, confs, labels):
    """
    Print detection results as a table
    """
    print("-" * 75)
    print(
        "{:<15} {:<15} {:<10} {:<10} {:<10} {:<10}".format(
            "Label", "Confidence", "Left", "Top", "Width", "Height"
        )
    )
    print("-" * 75)
    for bbox, conf, label in zip(bboxes, confs, labels):
        print("{:<15} {:<15} {:<10} {:<10} {:<10} {:<10}".format(label, conf, *bbox))
    print("-" * 75)


def parse(
    results: Any, image: Any, CONF_THRESH: float = 0.45
) -> Tuple[List[Any], List[Any], List[Any]]:
    """
    Extract the bounding box and image from the detection
    """

    classes = []
    confs = []
    bboxes = []
    H, W = image.shape[:2]

    # Resizing factor.
    x_factor = W / INPUT_WIDTH
    y_factor = H / INPUT_HEIGHT

    # Iterate through 25200 detections.
    for res in results:

        _conf = float(res[4])
        # Discard bad detections and continue.
        if _conf >= CONF_THRESH:
            scores = res[5:]

            # Get the index of max class score.
            _class = np.argmax(scores)

            #  Continue if the class score is above threshold.
            if scores[_class] > SCORE_THRESH:
                confs.append(_conf)
                classes.append(_class)

                cx, cy, w, h = res[0], res[1], res[2], res[3]

                left = int((cx - w / 2) * x_factor)
                top = int((cy - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                bboxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate overlapping boxes
    indices = cv2.dnn.NMSBoxes(bboxes, confs, CONF_THRESH, NMS_THRESH)

    bboxes = [bboxes[i] for i in indices]  # return left, top, width, height
    confs = [round(confs[i], 4) for i in indices]  # return confidences
    labels = [LABELS[classes[i]] for i in indices]  # return labels

    return bboxes, confs, labels


def detect(image, net, CONF_THRESH=0.45):
    """
    Detect objects in image
    """
    # Convert image to numpy array.
    image = np.array(image)

    # Create a blob from a frame.
    blob = cv2.dnn.blobFromImage(image, 1 / 255, (INPUT_WIDTH, INPUT_HEIGHT))

    # Sets the input to the network.
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers.
    out_layer = net.getUnconnectedOutLayersNames()
    results = net.forward(out_layer)[0][0]

    # Parse the output
    bboxes, confs, labels = parse(results, image, CONF_THRESH)

    return bboxes, confs, labels


def load_model(size):
    """
    Load trained model
    """

    net = cv2.dnn.readNet(f"./models/detect_{size}.onnx")
    return net


def check_speed(net):
    """
    Check the speed of the model in milliseconds
    """

    t, _ = net.getPerfProfile()
    freq = cv2.getTickFrequency()

    return (t * 1000) / freq


if __name__ == "__main__":
    # Create command line parser.
    parser = argparse.ArgumentParser(description="Detect objects in image")

    # Add arguments.
    parser.add_argument("--image", type=str, required=True, help="Path to image")
    parser.add_argument("--model", type=str, default="m", help="Model size to use (n, s, m, l, x)")
    parser.add_argument("--conf", type=float, default=0.5, help="Confidence threshold")
    parser.add_argument("--render", action="store_true", help="Render image with bounding boxes")

    # Parse arguments.
    args = parser.parse_args()

    try:
        print("[INFO] Reading image...")
        image = Image.open(args.image).convert("RGB")

        print("[INFO] Loading model...")
        net = load_model(args.model)

        print("[INFO] Detecting...")
        bboxes, confs, labels = detect(image, net, args.conf)
        print(f"[INFO] Inference: {check_speed(net):.2f} ms")

        print("[INFO] Detection...")
        print_detection(bboxes, confs, labels)

        if args.render:
            print("[INFO] Rendering...")
            image = render(image, bboxes, confs, labels)

            print("[INFO] Encoding image...")
            image_enc = encode_image(image)

            print("[INFO] Decoding image...")
            output = decode_image(image_enc)
            output.save(f"{args.image[:-4]}_out.png")
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)
